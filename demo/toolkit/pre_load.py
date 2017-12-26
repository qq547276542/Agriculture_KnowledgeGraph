# -*- coding: utf-8 -*-
import thulac
import csv
import sys
sys.path.append("..")
from Model.neo_models import Neo4j


pre_load_thu = thulac.thulac()  #默认模式

neo_con = Neo4j()   #预加载neo4j
neo_con.connectDB()

predict_labels = {}   # 预加载实体到标注的映射字典
with open('toolkit/predict_labels.txt','r') as csvfile:
	reader = csv.reader(csvfile, delimiter=' ')
	for row in reader:
		predict_labels[str(row[0])] = int(row[1])