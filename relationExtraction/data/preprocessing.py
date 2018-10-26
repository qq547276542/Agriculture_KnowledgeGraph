# -*- coding: utf-8 -*-
# 得到需要的一些json数据
import fire
import os
import json

cwd = os.getcwd()
class get_json_file():

    def __init__(self):
        self.relation_file_name = os.path.join(cwd,'staticResult.txt')
        self.relation_json_file_name = os.path.join(cwd,'rel2id.json')
        self.dataset_file_name = os.path.join(cwd,'filtered_data.txt')
        self.dataset_json_file_name = os.path.join(cwd,'dataset.json')
        self.word2vec_file_name = os.path.join(cwd,'sgns.wiki.bigram-char')
        self.word2vec_json_file_name = os.path.join(cwd,'word2vec.json')

    def get_rel_json(self):
        rel2id  = {0:'NA'}
        with open(self.relation_file_name,'r',encoding = 'utf8') as fr:
            for line in fr.readlines():
                try:
                    relation = line.split(',')[0]
                    relation = relation[2:len(relation)-1]
                    rel2id[len(rel2id)] = relation
                except:
                    raise ValueError
        with open(self.relation_json_file_name,'w') as fw:
            json.dump(rel2id,fw)

    def get_dataset_json(self):
        dataset = []
        with open(self.dataset_file_name,'r',encoding='utf8') as fr:
            for line in fr.readlines():
                try:
                    headpos,head,tailpos,tail,sentence,relation = line.split('\t')
                    sentence = sentence[1:len(sentence)-1]
                    dataset.append({'head':{'pos':headpos , 'word':head} , 'relation':relation, 'sentence':sentence ,'tail':\
                        {'pos':tailpos,'word':tail} } )
                except:
                    raise ValueError
        with open(self.dataset_json_file_name,'w',encoding='utf8') as fw:
            json.dump(dataset,fw)

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
                vec = line[index:-1]
                word2vec.append({'word':word,'vec':vec})

        with open(self.word2vec_json_file_name,'w',encoding= 'utf8') as fw:
            json.dump(word2vec,fw)








if __name__ == '__main__':
    get_json_file = get_json_file()
    fire.Fire({
        'rel2json':get_json_file.get_rel_json,
        'datasetjson':get_json_file.get_dataset_json,
        'word2vecjson':get_json_file.get_word2vec_json
    })
