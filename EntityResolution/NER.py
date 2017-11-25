# -*- coding: utf-8 -*-  
import thulac   
from py2neo import Graph,Node,Relationship

thu1 = thulac.thulac()  #默认模式
TagList = thu1.cut("芸香科柑橘亚科柑橘属，常绿小乔木。学名Citrus reticulata Blanco。", text=False) 

# 连接数据库
graph = Graph("http://localhost:7474", username="neo4j", password="8313178")

for line in TagList:
	title_value = line[0]
	answer = ""
	answer = graph.find_one(label="Item",property_key="title",property_value=title_value)
	if answer != None:
		print(answer['title'])
		print(answer['detail'])

#answer = graph.find_one(label="Item",property_key="title",property_value="橘")
#print(answer['detail'])