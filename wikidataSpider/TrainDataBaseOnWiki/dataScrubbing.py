# -*- coding: utf-8 -*-

import os
import sys
class DataScrubbing(object):
	#由extracTrainingData.py得到的数据无法直接使用，需要用该程序进行处理
	def __init__(self):
		self.pythonFilePath = os.path.abspath(os.getcwd()) 

	#部分句子有换行，把换行去掉
	#第一次产生的数据train_data.txt，由于之前程序在切割字符串时出了问题，因此relation这一列不对，这里重新处理一下
	#从所有训练集中挑选出与农业有关的数据

	#处理train_data.txt中存在的字符分割错误
	def handleRelationError(self,line):
		triplet = line.split('\t')
		if(len(triplet) != 4):
			print("Error! It's not a triplet!")
			return "Not a Triplet"
		else:
			relation = triplet[3]
			splitRelaton = relation.split("\"")
			relation = splitRelaton[1]
			tripletLine = triplet[0]+'\t'+triplet[1]+'\t'+triplet[2]+'\t'+relation
			return tripletLine.strip()

	#处理换行错误,flag=0表示出现换行错误的前一行,flag = 1 表示换行错误的后一行,将这两行拼接得到新的行
	def handleNewlineError(self,flag,replaceStr,fw,line,file):
		if(flag == 0):
			flag = 1 
			replaceStr = line.strip()
		else:
			newRecord = replaceStr+line.strip()
			if(file == "train_data.txt"):
				newRecord = self.handleRelationError(newRecord)
			if(newRecord != "Not a Triplet"):
				fw.write(newRecord+'\n')
			flag = 0
			replaceStr = ""

		return flag , replaceStr

	#处理一些错误的函数入口
	def handleError(self):
		for root,dirs,files in os.walk(self.pythonFilePath):
			for file in files:
				if(file[-3:] != "txt" or file=="fileReaded.txt"):
					continue
				print(file)
				count = 0 
				readFilePath = os.path.abspath(os.path.join(self.pythonFilePath,file))
				writeFilePath = os.path.abspath(os.path.join(self.pythonFilePath,file+"(2)"))
				with open(readFilePath,'r') as fr:
					with open(writeFilePath,'w') as fw:
						flag = 0
						replaceStr = ""
						for line in fr:
							#去掉文件头部(title)
							if(count ==0 ):
								count += 1
								continue
							if(count % 1000 ==0 ):
								print(count)
							count += 1
							triplet = line.split('\t') 
							if(len(triplet) != 4):
								flag,replaceStr = self.handleNewlineError(flag,replaceStr,fw,line,file)
								
							else:
								if(file == "train_data.txt"):
									line = self.handleRelationError(line)
								if(line != "Not a Triplet"):
									fw.write(line+'\n')
				os.remove(readFilePath)
				os.rename(writeFilePath,readFilePath)
    #选择和农业有关的训练集,选择关系"instance of" "taxon rank" "subclass of" "parent taxon"
	def selectAgricultureData(self):
		#预加载实体列表(挑选出如下类别的实体: 5:Animal,6:Plant,7:Chemicals,9:Food items,10:Diseases,12:Nutrients,13:Biochemistry.14:Agricultural implements,15:Technology )
		entityFilePath = os.path.abspath(os.path.join(self.pythonFilePath,"../wikientities/predict_labels.txt"))
		entitySet = set()
		with open(entityFilePath,'r') as fr:
			for line in fr:
				entityLine = line.strip().split()
				entity = entityLine[0]
				entityNumber = entityLine[1]
				if(entityNumber == "5" or entityNumber == "6" or entityNumber == "7" or entityNumber == "9" or entityNumber == "10" or entityNumber == "12" or entityNumber == "13" \
					or entityNumber == "14" or entityNumber == "15"):
					entitySet.add(entity)
		entityFilePath = os.path.abspath(os.path.join(self.pythonFilePath,"../wikientities/predict_labels2.txt"))
		
		with open(entityFilePath,'r') as fr:
			for line in fr:
				entityLine = line.strip().split()
				entity = entityLine[0]
				entityNumber = entityLine[1]
				if(entityNumber == "5" or entityNumber == "6" or entityNumber == "7" or entityNumber == "9" or entityNumber == "10" or entityNumber == "12" or entityNumber == "13" \
					or entityNumber == "14" or entityNumber == "15"):
					entitySet.add(entity)


		for root,dirs,files in os.walk(self.pythonFilePath):
			for file in files:
				if(file[-3:]!="txt" or file == "fileReaded.txt" or file == "entityrelation.txt" or file =="entitySet.txt"):
					continue
				count = 0
				#print(file)
				readFilePath = os.path.abspath(os.path.join(self.pythonFilePath,file))
				writeFilePath = os.path.abspath(os.path.join(self.pythonFilePath,file+"(2)"))
				with open(readFilePath,'r') as fr:
					with open(writeFilePath,'w') as fw:
						for line in fr:
							count+=1
							# if(count%1000):
							# 	print(count)
							triplet = line.strip().split('\t')
							if(len(triplet) == 4):
								entity1 = triplet[0]
								entity2 = triplet[1]
								statement = triplet[2]
								relation = triplet[3]
								if((relation == "instance of" or relation == "taxon rank" or relation == "subclass of" or relation =="parent taxon" ) and ((entity1 in entitySet) or \
								 (entity2 in entitySet))):
									fw.write(entity1+'\t'+entity2+'\t'+statement+'\t'+relation+'\n')
				os.remove(readFilePath)
				os.rename(writeFilePath,readFilePath)

if __name__ == "__main__":
	if(len(sys.argv) == 1):
		print("Missing parameters:  ")
		print("Please use \"python dataScrubbing.py handleError\" to solve error or use \"python dataScrubbing.py selectAgriculturalData\" to selecgt agricultural data ")
	elif(len(sys.argv) > 2):
		print("Too many parameters: ")
		print("Please use \"python dataScrubbing.py handleError\" to solve error or use \"python dataScrubbing.py selectAgriculturalData\" to selecgt agricultural data ")
	else:
		dataScrubbing = DataScrubbing()
		if(sys.argv[1] == "handleError"):
			dataScrubbing.handleError()
		elif(sys.argv[1] == "selectAgriculturalData"):
			dataScrubbing.selectAgricultureData()
		else:
			print("Parameter error: no such parameter")
			print("Please use \"python dataScrubbing.py handleError\" to solve error or use \"python dataScrubbing.py selectAgriculturalData\" to selecgt agricultural data ")


