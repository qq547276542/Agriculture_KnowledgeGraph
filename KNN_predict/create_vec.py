# coding: utf-8
# 将csv转化为词向量
from neo_models import Neo4j
from read_csv import readCSVbyColumn
from hudong_class import HudongItem
from pyfasttext import FastText

def create_predict(HudongItem_csv):
	# 读取neo4j内容 
	db = Neo4j()
	db.connectDB()
	
	predict_List = readCSVbyColumn(HudongItem_csv, 'title')
	file_object = open('vector.txt','a')
	
	model = FastText('wiki.zh.bin')
	
	count = 0
	vis = set()
	for p in predict_List:
		cur = HudongItem(db.matchHudongItembyTitle(p))
		count += 1
		title = cur.title
		if title in vis:
			continue
		vis.add(title)
		wv_list = model[title]
		strr = str(title)
		for p in wv_list:
			strr += ' '+str(p)[:7]
		file_object.write(strr+"\n")
		print(str(count)+' / '+str(len(predict_List)))
		
	file_object.close()
	
create_predict('hudong_pedia2.csv')
	