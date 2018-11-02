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


def get_explain(s):
	if s == 1:
		return '人物'
	if s == 2:
		return '地点'
	if s == 3:
		return r'机构'
	if s == 4:
		return '政治经济名词'
	if s == 5:
		return '动物学名词'
	if s == 6:
		return '植物学名词'
	if s == 7:
		return '化学名词'	
	if s == 8:
		return '季节气候'
	if s == 9:
		return '动植物产品'
	if s == 10:
		return '动植物疾病'
	if s == 11:
		return '自然灾害'
	if s == 12:
		return '营养成分'
	if s == 13:
		return '生物学名词'
	if s == 14:
		return '农机具'
	if s == 15:
		return '农业技术术语'	
	if s == 16:
		return '其它实体'	
	
	if s == 'np':
		return '人物'
	if s == 'ns':
		return '地点'	
	if s == 'ni':
		return '机构'
	if s == 'nz':
		return '专业名词'
	if s == 'i' or s == 'id':
		return '习语'
	if s == 'j':
		return '简称'
	if s == 'x':
		return '其它'
	if s == 't':
		return '时间日期'
		
	return '非实体'		


def get_detail_explain(s):
	if s == 1:
		return '包括人名，职位'
	if s == 2:
		return '包括地名，区域，行政区等'
	if s == 3:
		return '包括机构名，会议名，期刊名等'
	if s == 4:
		return '包括政府政策，政治术语，经济学术语'
	if s == 5:
		return '包括动物名称，动物类别，动物学相关术语'
	if s == 6:
		return '包括植物名称，植物类别，植物学相关术语'
	if s == 7:
		return '包括化肥，农药，杀菌剂，其它化学品，以及一些化学术语'	
	if s == 8:
		return '包括天气气候，季节，节气'
	if s == 9:
		return '包括肉制品，蔬菜制品，水果制品，豆制品等以动植物为原料的食品，以及一些非食物制品'
	if s == 10:
		return '包括传染病，原发性疾病，遗传病等'
	if s == 11:
		return '包括一些大型灾害，环境污染，或其它造成经济损失的自然现象'
	if s == 12:
		return '包括脂肪，矿物质，维生素，碳水化合物，无机盐等'
	if s == 13:
		return '包括人体部位，组织器官，基因相关，微生物，以及一些生物学术语'
	if s == 14:
		return '包括用于农业生产的自动化机械，手工工具'
	if s == 15:
		return '包括农学名词，农业技术措施'	
	if s == 16:
		return '与农业领域没有特别直接的关系，但是也是实体'	
		
	
	if s == 'np':
		return '包括人名，职位'
	if s == 'ns':
		return '包括地名，区域，行政区等'	
	if s == 'ni':
		return '包括机构名，会议名，期刊名等'
	if s == 'nz':
		return ' '
	if s == 'i' or s == 'id':
		return ' '
	if s == 'j':
		return ' '
	if s == 'x':
		return ' '
	if s == 't':
		return ' '
		
	return '非实体'	


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
		
	
# from toolkit.pre_load import pre_load_thu,neo_con
# print(get_NE(pre_load_thu, neo_con, '美利坚大香蕉习近平的橘子 hhhhhh'))