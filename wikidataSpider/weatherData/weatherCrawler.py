# -*- coding:utf-8 -*-

from urllib import request
from urllib import parse
from bs4 import BeautifulSoup
import json
from tqdm import tqdm
#得到互动百科页面
def get_hudong_page(word):
    res = request.urlopen("http://www.baike.com/wiki/"+parse.quote(word))
    return res.read().decode()

#得到互动百科页面介绍部分
def get_introduce(soup):
    summary = soup.find_all(class_ =  'summary')
    content = ""
    if(len(summary)>0):
        for p in summary:
            content+=p.text
        return content+'\n'
    else:
        return ""


if __name__ == '__main__':
    weather2weather = dict()
    weather_page  = dict()
    with open('weather2weather.txt','r',encoding='utf8') as fr:
        for line in fr.readlines():
            line_s = line.split('->')
            if(len(line_s) < 2):
                continue
            else:
                left_weather = line_s[0].strip()
                right_weather = line_s[1].strip()
                if(weather2weather.get(left_weather) is None):
                    weather2weather[left_weather] = right_weather
    weather_corpus = []
    with open('static_weather_list.txt','r',encoding='utf8') as fr:
        for line in tqdm(fr.readlines()):
            if(len(line)<2):
                continue
            line = line.strip()
            if(weather2weather.get(line) is not None):
                line = weather2weather[line]
            html = get_hudong_page(line)
            soup = BeautifulSoup(html,'lxml')
            title_list = []
            summary = get_introduce(soup)
            weather_page['summary'] = summary
            content = soup.find_all(id='content')
            if(len(content) > 0):
                weather_corpus.append({'title':line,'summary':summary,'content':content[0].text})
            else:
                print(line)
                print(content)

    with open('weather_corpus.json', 'w',encoding='utf8') as fw:
        json.dump(weather_corpus,fw,ensure_ascii=False)

