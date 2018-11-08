import json
import sys
sys.path.append("..")
import csv
import os
import re

from toolkit import NER
from Model import neo_models
from tqdm import tqdm

#加载各种气候的互动百科页面
with open('weather_corpus.json','r',encoding='utf8') as fr:
    weather_pedia = json.load(fr)


weather_dict = dict()
#加载其他气候到有百科页面的气候的映射
with open('weather2weather.txt','r',encoding='utf8') as fr:
    for line in fr.readlines():
        line_s = line.split('->')
        if(len(line_s) > 1):
            weather1 = line_s[0].strip()
            weather2 = line_s[1].strip()
            if(weather_dict.get(weather2) is None):
                weather_dict[weather2] = [weather1]
            else:
                weather_dict[weather2].append(weather1)


#预处理
predict_labels = {}   # 预加载实体到标注的映射字典
filePath = os.path.abspath(os.path.join(os.getcwd(),".."))

with open(filePath+'/toolkit/predict_labels.txt','r',encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile, delimiter=' ')
    for row in reader:
        predict_labels[str(row[0])] = int(row[1])
print('predicted labels load over!')

neo_con = neo_models.Neo4j()
neo_con.connectDB()
#判断传入的实体是否属于植物界
def find_plant(word):
    ret = neo_con.findEntityRelation(word, '界', '植物界')
    if(len(ret) !=0 ):
        return 1
    return 0
#识别气候百科页面对应的植物，查看是否是植物界
exclude_entity = ['植物']
with open('weather_plant.csv','w',encoding='utf8') as fw:
    fw.write("Weather"+","+"relation"+","+"Plant"+'\n')
    for line in tqdm(weather_pedia):
        weather = line['title'].strip()
        content = line['content'].strip()
        content = re.sub(r'\\',r'-',content)
        content = re.sub(r'\'','`',content)
        entities_list  = NER.get_NE(content)
        vis = []
        for entity in entities_list:
            word = entity[0]
            type = entity[1]
            if(type == 6 and word not in exclude_entity and word not in vis):
                vis.append(word)
                #查询是否是植物界
                plant = find_plant(word)
                if(plant == 1):
                    fw.write(weather+','+'适合种植'+','+word+'\n')
                    if(weather_dict.get(weather) is not None):
                        for x in weather_dict.get(weather):
                            fw.write(x+','+'适合种植'+','+word+'\n')



