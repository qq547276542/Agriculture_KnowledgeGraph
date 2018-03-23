# coding: utf-8
from classifier import Classifier
from neo_models import Neo4j
from read_csv import readCSVbyColumn
from hudong_class import HudongItem

def create_predict(HudongItem_csv):
	# 读取neo4j内容 
	db = Neo4j()
	db.connectDB()
	data_set = db.getLabeledHudongItem('labels.txt')
	classifier = Classifier('wiki.zh.bin')
	classifier.load_trainSet(data_set)     
	classifier.set_parameter(weight=[1.0, 3.0, 0.2, 4.0, 0],k=10)
	predict_List = readCSVbyColumn(HudongItem_csv, 'title')
	file_object = open('predict_labels2.txt','a')
	
	count = 0
	vis = set()
	for p in predict_List:
		cur = HudongItem(db.matchHudongItembyTitle(p))
		count += 1
		title = cur.title
		if title in vis:
			continue
		vis.add(title)
		label = classifier.KNN_predict(cur)
		print(str(title)+" "+str(label)+": "+str(count)+"/"+str(len(predict_List)))
		file_object.write(str(title)+" "+str(label)+"\n")
		
	file_object.close()
	
#create_predict('hudong_pedia2.csv')
	