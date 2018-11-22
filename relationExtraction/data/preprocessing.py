# -*- coding: utf-8 -*-
# 得到需要的一些json数据
import fire
import os
import json
import numpy as np

cwd = os.getcwd()
class get_json_file():

    def __init__(self):
        self.relation_file_name = os.path.join(cwd,'staticResult.txt')
        self.relation_json_file_name = os.path.join(cwd,'rel2id.json')
        self.dataset_file_name = os.path.join(cwd,'filtered_data.txt')
        self.dataset_json_file_name = os.path.join(cwd,'dataset.json')
        self.word2vec_file_name = os.path.join(cwd,'sgns.wiki.bigram-char')
        self.word2vec_json_file_name = os.path.join(cwd,'word2vec.json')
        self.entity_json_file_name = os.path.join(cwd,'entity2id.json')

    def get_rel_json(self):
        rel2id  = {'NA':0}
        relation_list = ['instance of', 'has part', 'subclass of', 'parent taxon', 'material used',
                         'natural product of taxon']

        #rel2id = {}
        for x in relation_list:
            rel2id[x] = len(rel2id)

        with open(self.relation_json_file_name,'w') as fw:
            json.dump(rel2id,fw,ensure_ascii=False,indent = 4, separators=(',', ': '))

    def get_dataset_json(self):
        dataset = []
        with open(self.entity_json_file_name,'r',encoding='utf8') as fr:
            entity2id = json.load(fr)
        with open(self.dataset_file_name,'r',encoding='utf8') as fr:

            for line in fr.readlines():
                try:
                    headpos,head,tailpos,tail,sentence,relation = line.split('\t')
                    if entity2id.get(head) is None:
                        headid = str(len(entity2id))
                    else:
                        headid = str(entity2id[head])
                    if entity2id.get(tail) is None:
                        tailid = str(len(entity2id))
                    else:
                        tailid = str(entity2id[tail])
                    #sentence = sentence[1:len(sentence)-1]
                    dataset.append({'head':{'pos':headpos , 'word':head.strip(),'id':headid} , 'relation':relation.strip(), 'sentence':sentence.strip(),'tail':\
                        {'pos':tailpos,'word':tail.strip(),'id':tailid} } )
                except:
                    raise ValueError
        with open(self.dataset_json_file_name,'w',encoding='utf8') as fw:
            json.dump(dataset,fw,ensure_ascii=False,indent = 4, separators=(',', ': '))

    def get_NA_dataset_json(self):
        na_dataset = []
        with open(self.entity_json_file_name,'r',encoding='utf8') as fr:
            entity2id = json.load(fr)
        with open('NA_SAMPLE.txt','r',encoding='utf8') as fr:
            with open('NA_dataset.json','w',encoding='utf8') as fw:
                for line in fr.readlines():
                    line = line.strip()
                    try:
                        headpos,head,tailpos,tail,sentence,relation = line.split('\t')
                        if entity2id.get(head) is None:
                            headid = str(len(entity2id))
                        else:
                            headid = str(entity2id[head])
                        if entity2id.get(tail) is None:
                            tailid = str(len(entity2id))
                        else:
                            tailid = str(entity2id[tail])
                        na_dataset.append({'head':{'pos':headpos,'word':head.strip(),'id':headid},'relation':relation.strip(),'sentence':sentence.strip(),'tail':\
                            {'pos':tailpos,'word':tail.strip(),'id':tailid} })
                    except:
                        raise ValueError

                json.dump(na_dataset,fw,ensure_ascii=False,indent=4,separators=(',',': '))




    def get_word2vec_json(self):
        word2vec = []
        with open(self.word2vec_file_name,'r',encoding = 'utf8') as fr:
            num,dim = fr.readline().split()
            print("%s words, %s dim"%(num,dim))
            while(True):
                line = fr.readline()
                if(not line):
                    break
                index = line.find(' ')
                word = line[0:index]
                vec = line[index:-1].strip().split()
                word2vec.append({'word':word ,'vec':vec})

        with open(self.word2vec_json_file_name,'w',encoding= 'utf8') as fw:
            json.dump(word2vec,fw,ensure_ascii=False, separators=(',',':'))

    # 给entity编号:
    def get_entity_id(self):
        cnt = 0
        entity2id = {}
        with open('entities.txt', 'r', encoding='utf8') as fr:
            for line in fr.readlines():
                line_s = line.split()
                if (entity2id.get(line_s[0].strip()) is None):
                    entity2id[line_s[0].strip()] = cnt
                    cnt += 1
        with open('entity2id.json', 'w', encoding='utf8') as fw:
            json.dump(entity2id, fw, ensure_ascii=False)


    # 将dataset.json分成train_dataset.json和test_dataset.json,给train_dataset.json和test_dataset.json加入一定数量的NA样本
    def train_test_split(self):
        train_na_number = 2000
        test_na_number = 500

        with open('dataset.json', 'r', encoding='utf8') as fr:
            dataset = json.load(fr)

        dataset_length = len(dataset)
        print("number of samples: ", dataset_length+train_na_number+test_na_number)
        train_dataset_length = int(0.8 * dataset_length)
        test_dataset_length = dataset_length - train_dataset_length

        print("number of training samples:", train_dataset_length+train_na_number)
        print("number of testing sample:", test_dataset_length+test_na_number)

        index = 0
        train_na_dataset = []
        test_na_dataset = []
        with open('NA_dataset.json','r',encoding='utf8') as fr:
            na_dataset = json.load(fr)
            print(len(na_dataset))
            for i in range(2000):
                train_na_dataset.append(na_dataset[index])
                index += 1

            for i in range(500):
                test_na_dataset.append(na_dataset[index])
                index += 1

        train_dataset = np.concatenate((dataset[0:train_dataset_length],train_na_dataset)).tolist()
        test_dataset = np.concatenate((dataset[train_dataset_length:dataset_length],test_na_dataset)).tolist()
        with open('train_dataset.json', 'w', encoding='utf8')as fw:
            json.dump(train_dataset,fw, ensure_ascii=False, indent=4, separators=(',', ': '))

        with open('test_dataset.json', 'w', encoding='utf8') as fw:
            json.dump(test_dataset, fw, ensure_ascii=False, indent=4,
                      separators=(',', ': '))

        # 统计train和test中的关系分布
        train_relation_dict = {}
        test_relation_dict = {}

        for x in train_dataset:
            relation = x['relation']
            if relation not in train_relation_dict:
                train_relation_dict[relation] = 1
            else:
                train_relation_dict[relation] += 1

        for x in test_dataset:
            relation = x['relation']
            if relation not in test_relation_dict:
                test_relation_dict[relation] = 1
            else:
                test_relation_dict[relation] += 1

        print("training samples relation number", train_relation_dict)
        print("testing samples relation number", test_relation_dict)





if __name__ == '__main__':
    get_json_file = get_json_file()
    fire.Fire({
        'rel2json':get_json_file.get_rel_json,
        'datasetjson':get_json_file.get_dataset_json,
        'word2vecjson':get_json_file.get_word2vec_json,
        'na_datasetjson':get_json_file.get_NA_dataset_json,
        "entity2id": get_json_file.get_entity_id,
        "dataset_split": get_json_file.train_test_split
    })
