# -*- coding:utf-8 -*-
import config
import tensorflow as tf
import os
import time
import numpy as np
import sys
import sklearn.metrics


class re_framework:
    #bag level
    MODE_BAG = 0
    #Instance level
    MODE_INS = 1

    def __init__(self,train_data_loader,test_data_loader,max_length = config.model.max_length,batch_size=config.model.batch_size):
        self.train_data_loader = train_data_loader
        self.test_data_loader = test_data_loader
        self.sess = None

    def __iter__(self):
        return self

    def average_gradients(self,tower_grads):
        '''
        多GPU,用于计算平均梯度
        :param tower_grads:tower_grads为一个列表，列表中的每一项都是一个tuple列表

        [ [(grad0,var0),(grad1,var1),...],[(grad0,var0),(grad1,var1),...] ]

        :return: 返回平均梯度，((avg_grad0,var0),(avg_grad1,var1),...)
        '''
        average_grads = []

        '''
        zip(*tower_grads)
        假设tower_grads = [[(1,0),(2,1),(3,2)],[(4,0),(5,1),(6,2)],[(7,0),(8,1),(9,2)]]
        zip(*tower_grads) = 
        [((1, 0), (4, 0), (7, 0)),
        ((2, 1), (5, 1), (8, 1)),
        ((3, 2), (6, 2), (9, 2))]
           
        '''
        for grad_and_vars in zip(*tower_grads):
            grads = []
            # 每个grad_and_vars 形如 ((grad0_gpu0, var0_gpu0), ... , (grad0_gpuN, var0_gpuN)) , ((grad1_gpu0,var1_gpu0),...,(grad1_gpuN,var1_gpuN))
            for g,_ in grad_and_vars:
                expand_g = tf.expand_dims(g,0)
                grads.append(expand_g)

            grad = tf.concat(grads,0)
            grad = tf.reduce_mean(grad,0)

            v= grad_and_vars[0][1]
            average_grads.append((grad,v))
        return average_grads

    def one_step_multi_models(self,models,batch_data_gen,run_array,return_label=True):
        feed_dict = {}
        batch_label = []
        for model in models:
            batch_data = batch_data_gen.next_batch(batch_data_gen.batch_size // len(models))
            feed_dict.update({
                model.word: batch_data['word'],
                model.pos1: batch_data['pos1'],
                model.pos2: batch_data['pos2'],
                model.label: batch_data['rel'],
                model.ins_label: batch_data['ins_rel'],
                model.scope: batch_data['scope'],
                model.length: batch_data['length'],
            })
            if 'mask' in batch_data and hasattr(model,"mask"):
                feed_dict.update({
                    model.mask: batch_data['mask']
                })
            batch_label.append(batch_data['rel'])
        result = self.sess.run(run_array,feed_dict)
        batch_label = np.concatenate(batch_label)
        if return_label:
            result += [batch_label]
        return result

    def one_step(self, model, batch_data, run_array):
        feed_dict = {
            model.word: batch_data['word'],
            model.pos1: batch_data['pos1'],
            model.pos2: batch_data['pos2'],
            model.label: batch_data['rel'],
            model.ins_label: batch_data['ins_rel'],
            model.scope: batch_data['scope'],
            model.length: batch_data['length'],
        }
        if 'mask' in batch_data and hasattr(model, "mask"):
            feed_dict.update({model.mask: batch_data['mask']})
        result = self.sess.run(run_array, feed_dict)
        return result

    def train(self,model,model_name,ckpt_dir = './checkpoint',summary_dir ='./summary',test_result_dir='./test_result',
              learning_rate = config.model.learning_rate,max_epoch = config.model.max_epoch,pretrain_model = None
              ,test_epoch = config.model.test_epoch ,optimizer = config.model.optimizer,gpu_list= config.model.gpu_list):

        gpu_nums = len(gpu_list)
        assert(self.train_data_loader.batch_size % gpu_nums == 0)
        print("start training...")

        #Init
        configure = tf.ConfigProto()
        configure.allow_soft_placement = True
        configure.gpu_options.allow_growth = True
        configure.gpu_options.per_process_gpu_memory_fraction = 1.0

        optimizer = optimizer(learning_rate)




        #for multi gpus
        tower_grads= []
        tower_models = []
        gpu_list = config.model.gpu_list
        for gpu_id in gpu_list:
            with tf.device("/gpu:%d" % gpu_id):
                with tf.name_scope("gpu_%d" % gpu_id):
                    self.sess = tf.Session(config=configure)
                    cur_model = model(self.train_data_loader,config.model.batch_size // gpu_nums,self.train_data_loader.max_length)
                    tower_grads.append(optimizer.compute_gradients(cur_model.loss()))
                    tower_models.append(cur_model)
                    tf.add_to_collection("loss",cur_model.loss())
                    tf.add_to_collection("train_logit",cur_model.train_logit())

        loss_collection = tf.get_collection("loss")
        loss = tf.add_n(loss_collection) / len(loss_collection)

        train_logit_collection = tf.get_collection("train_logit")
        train_logit = tf.concat(train_logit_collection,0)

        grads = self.average_gradients(tower_grads)
        train_op = optimizer.apply_gradients(grads)
        summary_writer = tf.summary.FileWriter(summary_dir,tf.get_default_graph())

        #Saver
        saver = tf.train.Saver(max_to_keep=None)

        if pretrain_model is None:
            self.sess.run(tf.global_variables_initializer())
        else:
            saver.restore(self.sess,pretrain_model)

        #Training
        best_metric = 0
        best_prec = None
        best_recall = None
        not_best_count = 0

        for epoch in range(max_epoch):
            print('###### Epoch' + str(epoch) + '######')
            tot_correct = 0
            tot_not_na_correct = 0
            tot = 0
            tot_not_na = 0
            i = 0
            time_sum = 0

            while True:
                time_start = time.time()
                try:
                    iter_loss, iter_logit,_train_op,iter_label = self.one_step_multi_models(tower_models,self.train_data_loader,[loss,train_logit,train_op])
                except StopIteration:
                    break

                time_end = time.time()

                t = time_end - time_start

                time_sum += t
                iter_output = iter_logit.argmax(-1)
                iter_correct = (iter_output == iter_label).sum()
                iter_correct = (iter_output == iter_label).sum()
                iter_not_na_correct = np.logical_and(iter_output == iter_label, iter_label != 0).sum()
                tot_correct += iter_correct
                tot_not_na_correct += iter_not_na_correct
                tot += iter_label.shape[0]
                tot_not_na += (iter_label != 0).sum()
                if tot_not_na > 0:
                    sys.stdout.write(
                        "epoch %d step %d time %.2f | loss: %f, not NA accuracy: %f, accuracy: %f\r" % (
                        epoch, i, t, iter_loss, float(tot_not_na_correct) / tot_not_na, float(tot_correct) / tot))
                    sys.stdout.flush()
                i += 1

            print("\nAverage iteration time: %f" % (time_sum / i))

            if (epoch+1)%test_epoch== 0:
                metric = self.test(model)
                if metric > best_metric:
                    best_metric = metric
                    best_prec = self.cur_prec
                    best_recall = self.cur_recall
                    print("Best Model, storing...")
                    if not os.path.isdir(ckpt_dir):
                        os.mkdir(ckpt_dir)
                    path = saver.save(self.sess,os.path.join(ckpt_dir,model_name),write_meta_graph=False)
                    print("Finish Storing")
                    not_best_count = 0
                else:
                    not_best_count += 1
                if not_best_count >=20:
                    break
        print("######")
        print("Finish training " + model_name)
        print("Best epoch auc = %f" %(best_metric))

        if (not best_prec is None) and (not best_recall is None):
            if not os.path.isdir(test_result_dir):
                os.mkdir(test_result_dir)

            np.save(os.path.join(test_result_dir,model_name+'_x.npy'),best_recall)
            np.save(os.path.join(test_result_dir,model_name+'_y.npy'),best_prec)


    def test(self,model,ckpt = None,return_result = False,mode=MODE_BAG):
        if mode == re_framework.MODE_BAG:
            return self.__test_bag__(model,ckpt=ckpt,return_result=return_result)


    def __test_bag__(self,model,ckpt=None,return_result = False):
        print("Testing...")
        gpu_id = config.model.gpu_list[0]
        with tf.device("/gpu:%d" % gpu_id):
            model = model(self.test_data_loader,self.test_data_loader.batch_size,self.test_data_loader.max_length)
            if not ckpt is None:
                saver = tf.train.Saver()
                saver.restore(self.sess,ckpt)
            tot_correct = 0
            tot_not_na_correct = 0
            tot =0
            tot_not_na = 0
            entpair_tot = 0
            test_result = []
            pred_result = []

            if self.sess == None:
                self.sess = tf.Session()
            for i,batch_data in enumerate(self.test_data_loader):
                iter_logit  = self.one_step(model,batch_data,[model.test_logit()])[0]
                iter_output = iter_logit.argmax(-1)
                iter_correct = (iter_output == batch_data['rel']).sum()
                iter_not_na_correct = np.logical_and(iter_output == batch_data['rel'],batch_data['rel']!=0).sum()
                tot_correct += iter_correct
                tot_not_na_correct += iter_not_na_correct
                tot += batch_data['rel'].shape[0]
                tot_not_na += (batch_data['rel'] != 0).sum()
                if tot_not_na > 0:
                    sys.stdout.write("[TEST] step %d | not NA accuracy: %f, accuracy: %f\r" % (
                    i, float(tot_not_na_correct) / tot_not_na, float(tot_correct) / tot))
                    sys.stdout.flush()

                for idx in range(len(iter_logit)):
                    for rel in range(1,self.test_data_loader.rel_tot):
                        test_result.append({'score':iter_logit[idx][rel],'flag':batch_data['multi_rel'][idx][rel]})
                        if batch_data['entpair'][idx] != "None#None":
                            pred_result.append({'score':iter_logit[idx][rel],'entpair':batch_data['entpair'][idx],'relation':rel})
                    entpair_tot +=1


            sorted_test_result = sorted(test_result,key=lambda x:x['score'])

            prec = []
            recall = []
            correct = 0

            for i,item in enumerate(sorted_test_result[::-1]):
                correct += item['flag']
                prec.append(float(correct)/(i+1))
                recall.append(float(correct)/ self.test_data_loader.relfact_tot )

            auc = sklearn.metrics.auc(x=recall, y=prec)
            print("\n[TEST] auc: {}".format(auc))
            print("Finish testing")
            self.cur_prec = prec
            self.cur_recall = recall

            if not return_result:
                return auc
            else:
                return (auc, pred_result)



