# -*- coding:utf-8 -*-
import fire
import json
import pandas as pd
import csv
def get_city_list():
    city_list = []
    with open('city.json','r',encoding='utf8') as fr:
        city_json = json.load(fr)

    for key in city_json:
        city_name = city_json[key]
        print(city_name)
        if(city_name[len(city_name)-1]  == '市' ):
            city_list.append(city_name)
              
    with open('city_list.txt','w',encoding = 'utf8') as fw:
        for line in city_list:
                fw.write(line+'\n')
#获取各个城市的气候信息
def get_city_weather():
    city_list = []
    with open('city_list.txt','r',encoding='utf8') as fr:
        for line in fr.readlines():
            city_list.append(line.strip())
            city_list.append(line.strip()[0:-1])

    data = pd.read_csv('../wikidataAnalyse/hudong_pedia.csv')
    with open('city_weather.txt','w',encoding='utf8') as fw:
        vis = []
        weather = []
        for i in range(len(data)):
            title = str(data['title'][i]).strip()
            if(title in city_list):
                info_key = str(data['baseInfoKeyList'][i]).strip()
                if(len(info_key) == 0):
                    continue
                info_value = str(data['baseInfoValueList'][i]).strip()
                info_key_list = info_key.split('##')
                info_value_list = info_value.split('##')
                cnt = 0
                for item in info_key_list:
                    if(item.strip() == '气候条件：' or item.strip() == '气候：' or item.strip() == '气候条件' or item.strip() == '气候'
                    or item.strip() == '气候条件:' or item.strip() == '气候:'):
                        if(title[-1]!='市'):
                            title+='市'
                        if(title not in vis):
                            vis.append(title)
                            if(info_value_list[cnt].strip().split('、')>1):
                                for x in info_value_list[cnt].strip().split('、'):
                                    if(x not in weather):
                                        weather.append(x)
                                    fw.write(title + "\t" + x + '\n')

                            else:
                                if(info_value_list[cnt].strip() not in weather):
                                    weather.append(info_value_list[cnt].strip())
                                fw.write(title+"\t"+info_value_list[cnt].strip()+'\n')
                    cnt += 1

    with open('static_weather_list.txt','w',encoding='utf8') as fw:
        for item in weather:
            fw.write(item+'\n')



if __name__ == '__main__':
    fire.Fire()
