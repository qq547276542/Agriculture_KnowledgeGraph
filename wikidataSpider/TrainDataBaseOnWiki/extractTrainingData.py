# -*- coding: utf-8 -*-

import os
import thulac
import sys
sys.path.append("..")
from toolkit.pre_load import pre_load_thu,neo_con,predict_labels
from toolkit.NER import get_NE,temporaryok,get_explain,get_detail_explain
import json
#分句标识符号
stopToken = "。！？"
def CutStatements(line):
	statements = []
	tokens = []
	for token in line:
		tokens.append(token)
		#如果是句子停止词
		if(token in stopToken):			
			statements.append(''.join(tokens))
			tokens = []
	if( len(tokens)>2 ):
		statements.append(''.join(tokens)+"。")
	return statements

thu = pre_load_thu #预先加载好
#连接数据库
db = neo_con

corpusPath = os.path.abspath(os.path.join(os.getcwd(),"../wikiextractor/extracted/"))
#获取已经处理过得文件
fileReadedList = []
with open("fileReaded.txt","r") as fileReaded:
	for line in fileReaded:
		fileReadedList.append(line.strip())
		print(line.strip())
#递归遍历语料库文件夹
with open("train_data6.txt",'w') as fw:
	with open("fileReaded.txt","a") as filereaded:
		fw.write('entity1\tentity2\tstatement\trelation\n')
		#存储已经搜索过的实体，避免重复查询
		entityRelationDict = {}
		for root,dirs,files in os.walk(corpusPath):			
			for file in files:
				filePath = os.path.join(root,file)
				if(filePath in fileReadedList):
					continue
				if(len(file) > 7 and file[-7:] == 'zh_hans' ):
					with open(filePath,'r') as fr:
						count = 0
						for line in fr:
							count += 1
							if(count%100 == 0):
								print(filePath+"  "+str(count))
							#过滤掉<doc >  </doc> 等无用行
							if(len(line)< 2 or line[0:4] == '<doc' or line[0:6] == "</doc>"):
								continue
							#分句
							statements = CutStatements(line)
							for statement in statements:
								#分词
								cutResult = get_NE(statement.strip())
								#得到每句话的实体列表后，两两匹配查询是否具有某种关系,如果有的话就写到文件中
								entityList = []
								for word in cutResult:
									if(word[1]!=0 and not temporaryok(word[1])):
										entityList.append(word[0])
								entityNumber = len(entityList)
								for i in range(entityNumber):
									answer = None
									answer = entityRelationDict.get(entityList[i])
									if(entityRelationDict.get(entityList[i]) is None):
										answer = db.findRelationBetweenEntities(entityList[i])
										entityRelationDict[entityList[i]] = answer
									for relation in answer:
										rel = str(relation['rel']).split("\"")[1]
										n2 = str(relation['n2'])
										index = n2.find('title')
										flag = 0
										entity2 = str()
										while(flag < 2 ):
											if(n2[index] == "\"" and flag == 0):
												flag += 1
											elif(n2[index] == "\"" and flag == 1):
												flag += 1
											elif(flag == 1):
												entity2 = entity2+n2[index]
											index += 1
										#与entity1相关联的实体也出现在同一句话中，则可以制造一条训练样本
										if(entity2 in entityList):
											fw.write(entityList[i]+'\t'+entity2+'\t'+statement.strip()+'\t'+rel+'\n')

					filereaded.write(filePath+'\n')
									

					
				


