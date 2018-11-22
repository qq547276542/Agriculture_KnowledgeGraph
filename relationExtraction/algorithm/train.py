import module
import os
import sys
import config
import tensorflow as tf
import numpy as np

dataset = "nyt"
if(len(sys.argv) > 1):
    data_set = sys.argv[1]


dataset_dir = config.dir.dataset_dir[dataset]['root']

if(not os.path.isdir(dataset_dir)):
    raise Exception("[ERROR] Dataset dir %s doesn't exit!" % dataset_dir)




#加载数据

train_loader = module.data_loader.json_file_data_loader(config.dir.dataset_dir['agriculture']['train'],
                                                        config.dir.dataset_dir['agriculture']['word2vec'],
                                                        config.dir.dataset_dir['agriculture']['rel2id'],
                                                        mode = config.model.train_level,
                                                        shuffle = True)

test_loader = module.data_loader.json_file_data_loader(config.dir.dataset_dir['agriculture']['test'],
                                                       config.dir.dataset_dir['agriculture']['word2vec'],
                                                       config.dir.dataset_dir['agriculture']['rel2id'],
                                                       mode = config.model.test_level,
                                                       shuffle =False)


framework = module.framework.re_framework(train_loader,test_loader)

class model:
    encoder = config.model.encoder

    def __init__(self,train_data_loader,batch_size,max_length):
        self.word = tf.placeholder(dtype=tf.int32,shape=[None,max_length], name = 'word')
        self.pos1 = tf.placeholder(dtype=tf.int32,shape=[None,max_length], name = 'pos1')
        self.pos2 = tf.placeholder(dtype=tf.int32,shape=[None,max_length], name = 'pos2')
        self.label = tf.placeholder(dtype=tf.int32,shape=[batch_size], name = 'label')
        self.ins_label = tf.placeholder(dtype=tf.int32,shape=[None],name = 'ins_label')
        self.length = tf.placeholder(dtype=tf.int32,shape=[None],name='length')
        self.scope = tf.placeholder(dtype=tf.int32,shape=[batch_size,2],name='scope')
        self.train_data_loader = train_data_loader
        self.rel_tot = train_data_loader.rel_tot
        self.word_vec_mat = train_data_loader.word_vec_mat

        self.mask = tf.placeholder(dtype=tf.int32,shape=[None,max_length],name='mask')

        # Embedding layer
        x = module.network.embedding.word_position_embedding(self.word,self.word_vec_mat,self.pos1,self.pos2)

        # Encoder
        x_train = module.network.encoder.pcnn(x,self.mask,keep_prob = 0.5)
        x_test = module.network.encoder.pcnn(x,self.mask,keep_prob = 1.0)

        #Selector
        self._train_logit , train_repre = module.network.selector.bag_average(x_train,self.scope,self.rel_tot,True,keep_prob=0.5)
        self._test_logit,test_repre = module.network.selector.bag_average(x_test,self.scope,self.rel_tot)
        self._test_logit = tf.nn.softmax(self._test_logit)
        #classifier
        self._loss = module.network.classifier.softmax_cross_entropy(self._train_logit,self.label,self.rel_tot,weights_table=self.get_weights())

    def loss(self):
        return self._loss
    def train_logit(self):
        return self._train_logit
    def test_logit(self):
        return self._test_logit

    def get_weights(self):
        with tf.variable_scope("weights_table", reuse=tf.AUTO_REUSE):
            print("Calculating weights_table...")
            _weights_table = np.zeros((self.rel_tot), dtype=np.float32)
            for i in range(len(self.train_data_loader.data_rel)):
                _weights_table[self.train_data_loader.data_rel[i]] += 1.0
            _weights_table = 1 / (_weights_table ** 0.05)
            weights_table = tf.get_variable(name='weights_table', dtype=tf.float32, trainable=False, initializer=_weights_table)
            print("Finish calculating")
        return weights_table

if len(sys.argv) > 2:
    model.encoder = sys.argv[2]

framework.train(model,ckpt_dir = "checkpoint", model_name = dataset + "_" + model.encoder,max_epoch = config.model.max_epoch,gpu_list = config.model.gpu_list)