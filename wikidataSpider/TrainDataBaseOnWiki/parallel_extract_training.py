# -*- coding:utf-8 -*-

# 并行得到训练样本（主要是获得NA关系，因为其他的关系之前已经获取过了，这里不重复)
import os
import thulac
import sys
import fire
import json
sys.path.append("..")
import thulac
import csv
import numpy as np

from multiprocessing import Pool
from multiprocessing import Manager
from multiprocessing import cpu_count
from tqdm import tqdm

pre_load_thu = thulac.thulac()

predict_labels = {}   # 预加载实体到标注的映射字典
with open('predict_labels.txt','r',encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile, delimiter=' ')
    for row in reader:
        predict_labels[str(row[0])] = int(row[1])

def preok(s):  #上一个词的词性筛选
    
    if s=='n' or s=='np' or s=='ns' or s=='ni' or s=='nz':
        return True
    if s=='v' or s=='a' or s=='i' or s=='j' or s=='x' or s=='id' or s=='g' or s=='u':
        return True
    if s=='t' or s=='m':
        return True
    return False

def nowok(s): #当前词的词性筛选
    
    if s=='n' or s=='np' or s=='ns' or s=='ni' or s=='nz':
        return True
    if s=='a' or s=='i' or s=='j' or s=='x' or s=='id' or s=='g' or s=='t':
        return True
    if s=='t' or s=='m':
        return True
    return False
def temporaryok(s):  # 一些暂时确定是名词短语的（数据库中可以没有）
    if s=='np' or s=='ns' or s=='ni' or s=='nz':
        return True
    if s=='j' or s=='x' or s=='t':
        return True
    return False

def get_NE(text):
    # 读取thulac，neo4j，分词
    thu1 = pre_load_thu

    TagList = thu1.cut(text, text=False)
    TagList.append(['===',None])  #末尾加个不合法的，后面好写
    
    # 读取实体类别,注意要和predict_labels.txt一个目录
    label = predict_labels
    
    answerList = []
    i = 0
    length = len(TagList) - 1 # 扣掉多加的那个
    while i < length:
        p1 = TagList[i][0]
        t1 = TagList[i][1]
        p2 = TagList[i+1][0]
        t2 = TagList[i+1][1]
        p12 = p1 + TagList[i+1][0]
        
        # 不但需要txt中有实体，还需要判断数据库中有没有
        if p12 in label and preok(t1) and nowok(t2):  # 组合2个词如果得到实体
            answerList.append([p12,label[p12]])
            i += 2
            continue
    
        if p1 in label and nowok(t1):     # 当前词如果是实体
            answerList.append([p1,label[p1]])
            i += 1
            continue
        
        if temporaryok(t1):
            answerList.append([p1,t1])
            i += 1
            continue
        
        answerList.append([p1,0])
        i += 1
    
    return answerList

#分句标识符号
stop_token = "。！？"

def cut_statement(line):
    statements = []
    tokens = []
    for token in line:
        tokens.append(token)
        #如果是句子停止词
        if(token in stop_token):
            statements.append(''.join(tokens))
            tokens = []
    if( len(tokens)>2 ):
        st =''.join(tokens)+"。"
        statements.append(st)
    return statements

thu = pre_load_thu

corpus_path = os.path.abspath(os.path.join(os.getcwd(),"../wikiextractor/extracted/"))

#得到corpus_path路径下的所有文件名
file_name_list = []
for root,dirs,files in os.walk(corpus_path):
    for file in files:
        file_path = os.path.join(root,file)
        if (len(file)>7 and file[-7:] == 'zh_hans'):
            file_name_list.append(file_path)




#并行处理，得到NA样本
with open('entity2id.json','r',encoding='utf8') as fr:
    entity2id = json.load(fr)

with open('no_relation_pairs.txt','r',encoding='utf8') as fr:
    no_relation_pairs = []
    for line in fr:
        line_s = line.split()
        id1 = entity2id[line_s[0].strip()]
        id2 = entity2id[line_s[1].strip()]
        if((id1,id2) not in no_relation_pairs):
            no_relation_pairs.append((id1,id2))
            no_relation_pairs.append((id2,id1))
print(len(no_relation_pairs))
def process_file(lines):
    ret = []
    for line in lines:
        #过滤掉<doc >  </doc> 等无用行
        if(len(line)< 2 or line[0:4] == '<doc' or line[0:6] == "</doc>"):
            continue
        #分句
        statements = cut_statement(line)
        for statement in statements:
            #分词
            cutResult = get_NE(statement.strip())
            #得到每句话的实体列表后，两两匹配查询是否具有某种关系,如果有的话就写到文件中
            #entityList 存储实体列表和实体出现的位置,entity1存储实体名称，entity1Index存储实体位置
            entityList = []
            nowIndex = -1
            for word in cutResult:
                if(word[1]!=0 and not temporaryok(word[1])):
                    entity1Index = statement.index(word[0],nowIndex+1)
                    entityList.append({'entity1':word[0],'entity1Index':entity1Index})
                    nowIndex = entity1Index+len(word[0])-1

            entityNumber = len(entityList)
            #遍历所有实体对，找到没有关系的实体，写入文件
            for i in range(entityNumber):
                for j in range(i+1,entityNumber):
                    id1 = entity2id[entityList[i]['entity1']]
                    id2 = entity2id[entityList[j]['entity1']]
                    if((id1,id2) in no_relation_pairs):
                        ret.append(str(entityList[i]['entity1Index'])+'\t'+entityList[i]['entity1'] + '\t' +str(entityList[j]['entity1Index'])+'\t'+entityList[j]['entity1']+'\t'+statement.strip()+'\t'+'NA'+'\t'+'\n')
    return np.array(ret)



def get_na_samples():
    cpu_num = cpu_count()
    pool = Pool(int(cpu_num/4))
    result = None
    with open("NA_sample_big.txt",'w',encoding = 'utf8') as fw:
        for file in tqdm(file_name_list):
            with open(file,'r',encoding='utf8') as fr:
                lines = fr.readlines()
                data_split = np.array_split(lines,int(cpu_num/4))
                if(result is None):
                    result = np.concatenate(pool.map(process_file,data_split))
                else:
                    tmp = np.concatenate(pool.map(process_file,data_split))
                    result  = np.concatenate((result,tmp))

    pool.close()
    pool.join()
    print(len(result))
    with open('NA_SAMPLE.txt','w',encoding='utf8') as fw:
        for line in result:
            fw.write(str(line)+'\n')

if __name__ == "__main__":
    get_na_samples()
