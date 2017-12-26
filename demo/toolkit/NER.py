# -*- coding: utf-8 -*-
import sys
import csv
sys.path.append("..")		
from toolkit.pre_load import pre_load_thu,neo_con,predict_labels

def preok(s):  #上一个词的词性筛选
	
	if s=='n' or s=='np' or s=='ns' or s=='ni' or s=='nz':
		return True
	if s=='v' or s=='a' or s=='i' or s=='j' or s=='x' or s=='id' or s=='g' or s=='u':
		return True
	if s=='t' or s=='m':
		return True
	return False
	
def nowok(s): #当前词的词性筛选
	
	if s=='n' or s=='np' or s=='ns' or s=='ni' or s=='nz':
		return True
	if s=='a' or s=='i' or s=='j' or s=='x' or s=='id' or s=='g' or s=='t':
		return True
	if s=='t' or s=='m':
		return True
	return False	

def temporaryok(s):  # 一些暂时确定是名词短语的（数据库中可以没有）
	if s=='np' or s=='ns' or s=='ni' or s=='nz':
		return True
	if s=='j' or s=='x' or s=='t':
		return True
	return False

# 前两个参数为thulac预加载好的模型，和已连接的neo4j
# text为文本，根据文本返回实体列表
# 返回二维数组 [N][2]，代表一句话分为若干的词（词组），以及该词组是否是命名实体
# 返回的1~16代表数据库中存在的命名实体，0代表非实体
# 返回的'np','ns'等英文代表返回的是数据库中不存在的命名实体
def get_NE(text):
	# 读取thulac，neo4j，分词
	thu1 = pre_load_thu
	db = neo_con
	TagList = thu1.cut(text, text=False)
	TagList.append(['===',None])  #末尾加个不合法的，后面好写
	
	# 读取实体类别,注意要和predict_labels.txt一个目录
	label = predict_labels
	
	answerList = []		
	i = 0
	length = len(TagList) - 1 # 扣掉多加的那个
	while i < length:
		p1 = TagList[i][0]
		t1 = TagList[i][1]
		p2 = TagList[i+1][0]
		t2 = TagList[i+1][1]
		p12 = p1 + TagList[i+1][0]
		
		# 不但需要txt中有实体，还需要判断数据库中有没有
		flag = db.matchHudongItembyTitle(p12) 
		if p12 in label and flag != None and preok(t1) and nowok(t2):  # 组合2个词如果得到实体
			answerList.append([p12,label[p12]])
			i += 2
			continue
		
		flag = db.matchHudongItembyTitle(p1)
		if p1 in label and flag != None and nowok(t1):	 # 当前词如果是实体
			answerList.append([p1,label[p1]])
			i += 1
			continue
		
		if temporaryok(t1):
			answerList.append([p1,t1])
			i += 1
			continue
			
		answerList.append([p1,0])
		i += 1
		
	return answerList
			

	
#from toolkit.pre_load import pre_load_thu,neo_con
#print(get_NE(pre_load_thu, neo_con, '美利坚大香蕉习近平的橘子 hhhhhh'))