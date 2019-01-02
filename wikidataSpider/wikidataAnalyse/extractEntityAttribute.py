import csv
import os
import sys
filePath = os.path.abspath(os.path.join(os.getcwd(),".."))
sys.path.append(filePath)

#from toolkit.pre_load import neo_con
# #连接neo4j数据库
# neo4j = neo_con
# def getEntityByName(entity):
# 	try:
# 		answer = neo_con.graph.data("MATCH (entity) WHERE entity.title = \""+entity+"\" RETURN entity")
# 		if(len(answer) >0):
# 			return 1
# 		else:
# 			return 0
# 	except:
# 		return 0

#加载实体列表
entitySet = set()
with open(filePath+"/wikidataProcessing/new_node.csv",'r') as fr:
	newNodeCsv = csv.reader(fr)
	for item in newNodeCsv:
		entitySet.add(item[0].strip())
with open(filePath+"/wikientities/predict_labels.txt",'r') as fr:
	for line in fr:
		predictLabel = line.split()[0]
		entitySet.add(predictLabel) 

with open('hudong_pedia.csv','r') as fr:
	with open('attributes.csv','w') as fw:
		fw.write('Entity'+','+'AttributeName'+','+'Attribute'+'\n')
		#从hudong_pedia.csv中提取出属性
		hudongPedia = csv.reader(fr)
		hudongPediaLineNum = 113037
		count = 0
		for item in hudongPedia:
			if(item[5] == "baseInfoKeyList"):
				continue
			count += 1
			if(count % 10 == 0):
				print(1.0*count/hudongPediaLineNum)
			baseInfoKeyList = item[5].split("##")
			baseInfoValueList = item[6].split('##')
			baseInfoKeyLength = len(baseInfoKeyList)
			baseInfoValueLength = len(baseInfoValueList)
			entityName = item[0]
			if( baseInfoKeyLength== baseInfoValueLength):
				for i in range(baseInfoValueLength):
					baseInfoKey = baseInfoKeyList[i].strip()
					if(len(baseInfoKey) == 0):
						continue
					if(baseInfoKey[-1] == "："):
						baseInfoKey = baseInfoKey[0:-1]
					baseInfoValue = baseInfoValueList[i].strip()
					if(len(baseInfoValue) == 0):
						continue
					if(baseInfoValue[-1] == "："):
						baseInfoValue = baseInfoValue[0:-1]	

					#如果实体名和baseInfoValue一样，则continue
					if(entityName == baseInfoValue):
						continue
					# invalidStringList = ["\"",".", "node labels", '[', "=~", "IN", "STARTS", "ENDS", "CONTAINS", "IS", "^", "*", "/", "%", "+", "-", "=", "<>", "!=", "<", ">", "<=", ">=", \
					# "AND", "XOR", "OR", "LOAD CSV", "FROM", "INTO", "START", "MATCH", "UNWIND", "MERGE", "CREATE GRAPH >>", "CREATE >> GRAPH", "CREATE GRAPH", "CREATE", "SET", "DELETE GRAPHS", "DELETE", \
					# "REMOVE", "FOREACH", "WITH", "CALL", "PERSIST", "RELOCATE", "RETURN", "SNAPSHOT", "UNION", ";" ,"end of input","\\"]
					# flag = 1
					# for invalidString in invalidStringList:
					# 	if(baseInfoKey.find(invalidString) !=-1 ):
					# 		flag = 0
					# 		break
					# 	if(baseInfoValue.find(invalidString) !=-1):
					# 		flag = 0
					# 		break 

					# if(flag == 0):
					# 	continue 

					# #查询属性是否在现有实体库中，如果没有，则忽略；否则，写入新的关系表中
					# answer = getEntityByName(baseInfoValue)
					# if(answer == 1):
					# 	fw.write(entityName+","+baseInfoKey+","+baseInfoValue+'\n')

					#查询属性是否在现有实体库中，如果没有，则忽略；否则，写入新的关系表中
					if(baseInfoValue in entitySet):
						fw.write(entityName+","+baseInfoKey+","+baseInfoValue+'\n')

			