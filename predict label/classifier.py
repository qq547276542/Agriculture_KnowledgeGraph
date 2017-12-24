# coding: utf-8

from hudong_class import HudongItem
from neo_models import Neo4j
from pyfasttext import FastText
from functools import cmp_to_key
from math import log
from math import sqrt

class Node:
	simi = None
	label = None
	title = None
	
	def __init__(self, s, l, t):
		self.simi = s
		self.label = l
		self.title = t
		

class Classifier:
	model = None
	labeled_hudongList = None
	mean = None    #各分量的均值
	var = None   #各分量的方差
	title_simi = None
	openTypeList_simi = None
	baseInfoKeyList_simi = None
	baseInfoValueList_simi = None
	
	openTypeList_IDF = None   # 逆文本频率指数  用于给开发类别和属性名加权
	baseInfoKeyList_IDF = None
	
	openTypeList_num = None   # 拥有开放类别和基本属性的 item数量
	baseInfoKeyList_num = None
	
	# 相似度权值，分别为：title，openTypeList，baseInfoKeyList，baseInfoValueList，detail
	weight = [0.2,0.2,0.2,0.2,0.2]  
	# knn的k值
	k = 10 
	
	
	def __init__(self,model_path): # 传入模型路径
		self.model = FastText(model_path)			
		print('classifier load over...')
		
	def load_trainSet(self,HudongList):  # 传入已经标注过的hudongItem列表
		self.labeled_hudongList = HudongList
		self.openTypeList_IDF = {}
		self.baseInfoKeyList_IDF = {}
		self.openTypeList_num = 0
		self.baseInfoKeyList_num = 0
		# 统计各个开放类别和属性的 IDF值
		for p in self.labeled_hudongList:
			if len(p.openTypeList) > 0:
				self.openTypeList_num += 1
			for t in p.openTypeList:
				if t in self.openTypeList_IDF:
					self.openTypeList_IDF[t] += 1
				else:
					self.openTypeList_IDF[t] = 1
			
			if len(p.baseInfoKeyList) > 0:
				self.baseInfoKeyList_num += 1
			for t in p.baseInfoKeyList:
				if t in self.baseInfoKeyList_IDF:
					self.baseInfoKeyList_IDF[t] += 1
				else:
					self.baseInfoKeyList_IDF[t] = 1
					
		for p in self.openTypeList_IDF:
			self.openTypeList_IDF[p] = log(1.0 * self.openTypeList_num / self.openTypeList_IDF[p])
			#print(str(p)+"---"+str(self.openTypeList_IDF[p]))
			
		for p in self.baseInfoKeyList_IDF:
			self.baseInfoKeyList_IDF[p] = log(1.0 * self.baseInfoKeyList_num / self.baseInfoKeyList_IDF[p])
			#print(str(p)+"---"+str(self.baseInfoKeyList_IDF[p]))

		
	def set_parameter(self,weight,k):  # 设置超参数
		self.weight = weight
		self.k = k
		
	# 返回2个item的titles相似度
	def get_title_simi(self,item1,item2):
		title_simi = self.model.similarity(item1.title,item2.title)
		return title_simi
		
	# 返回2个item的openTypeLis相似度
	def get_openTypeList_simi(self,item1,item2):
		openTypeList_simi = 0.0
		L1 = item1.openTypeList[:10]  #取前10个开放类别足够
		L2 = item2.openTypeList[:10]
		for p1 in L1:   #两组开放类别之间两两比较相似度，求和，求平均
			for p2 in L2:
				cur = self.model.similarity(p1,p2)
				openTypeList_simi += cur
		
		fm = len(L1)*len(L2)
		if fm > 0:
			openTypeList_simi /= fm
		
		return openTypeList_simi
		
	# 返回2个item的baseInfoKeyList相似度	
	def get_baseInfoKeyList_simi(self,item1,item2):
		baseInfoKeyList_simi = 0.0   # 基本信息的属性名之间 求jaccard相似系数
		s1 = set()
		s2 = set()
		for p in item1.baseInfoKeyList:
			s1.add(p)
		for p in item2.baseInfoKeyList:
			s2.add(p)
		and12 = s1&s2
		or12 = s1|s2
		fz = 0.0
		for p in and12:
			fz += self.baseInfoKeyList_IDF[p]
#		if len(or12)>0:
#			baseInfoKeyList_simi = 1.0*len(and12)/len(or12)
		baseInfoKeyList_simi = fz
		return baseInfoKeyList_simi
	
	# 返回2个item的baseInfoValueList相似度
	def get_baseInfoValueList_simi(self,item1,item2):
		s1 = set()
		s2 = set()
		dict1 = {}  
		dict2 = {}
		count = 0
		for p in item1.baseInfoKeyList:
			s1.add(p)
			if count < len(item1.baseInfoValueList):
				dict1[p] = item1.baseInfoValueList[count]
			count += 1
		count = 0
		for p in item2.baseInfoKeyList:
			s2.add(p)
			if count < len(item2.baseInfoValueList):
				dict2[p] = item2.baseInfoValueList[count]
			count += 1
		and12 = s1&s2
			
		baseInfoValueList_simi = 0.0  # 基本信息的属性名相同的属性值，对应值相似度求平均
		for s in and12:
			if s in dict1 and s in dict2 and dict1[s] == dict2[s] and s in self.baseInfoKeyList_IDF:
				baseInfoValueList_simi += 1.0*self.baseInfoKeyList_IDF[s]
#		if len(and12)>0:
#			baseInfoValueList_simi /= len(and12)
			
		return baseInfoValueList_simi	

    #暂时不用
	def similarity(self,item1,item2):  # 比较两个页面的相似度，返回[-1,1]之间的相似度
		title_simi = self.model.similarity(item1.title,item2.title)
		
		openTypeList_simi = 0.0
		for p1 in item1.openTypeList:   #两组开放类别之间两两比较相似度，求和，求平均
			for p2 in item2.openTypeList:
				openTypeList_simi += self.model.similarity(p1,p2)
		fm = len(item1.openTypeList)*len(item2.openTypeList)
		if fm > 0:
			openTypeList_simi /= fm
			
		baseInfoKeyList_simi = 0.0   # 基本信息的属性名之间 求jaccard相似系数
		s1 = set()
		s2 = set()
		dict1 = {}  
		dict2 = {}
		count = 0
		for p in item1.baseInfoKeyList:
			s1.add(p)
			dict1[p] = item1.baseInfoValueList[count]
			count += 1
		count = 0
		for p in item2.baseInfoKeyList:
			s2.add(p)
			dict2[p] = item2.baseInfoValueList[count]
			count += 1
		and12 = s1&s2
		or12 = s1|s2
		if len(or12)>0:
			baseInfoKeyList_simi = 1.0*len(and12)/len(or12)
			
		baseInfoValueList_simi = 0.0  # 基本信息的属性名相同的属性值，对应值相似度求平均
		for s in and12:
			baseInfoValueList_simi += self.model.similarity(dict1[s],dict2[s])
		if len(and12)>0:
			baseInfoValueList_simi /= len(and12)	
			
#		d1 = item1.detail[:60]   #只判断前60个字，降低复杂度
#		d2 = item2.detail[:60]
#		detail_simi = self.model.similarity(d1,d2)
				
		
		# 各组相似度线性加权
		simi = self.weight[0]*title_simi + self.weight[1]*openTypeList_simi + self.weight[2]*baseInfoKeyList_simi + self.weight[3]*baseInfoValueList_simi
		
		return simi
		
		
	def KNN_predict(self,item): # 预测互动页面的类别
		curList = [] # 用于存储和item相似度的临时列表
		
		mean = [0.,0.,0.,0.,0.]    #各分量的均值
		var = [0.,0.,0.,0.,0.]   #各分量的方差
		stand = [0.,0.,0.,0.,0.]  #各分量的标准差
		maxx = [-2333.3,-2333.3,-2333.3,-2333.3,-2333.3]
		minn = [2333.3,2333.3,2333.3,2333.3,2333.3]
		title_simi = [] 
		openTypeList_simi = []
		baseInfoKeyList_simi = []  
		baseInfoValueList_simi = []
		
		i = 0
		for p in self.labeled_hudongList:  # 预先计算存储各分量相似度
			if p.title == item.title:	# 如果训练集已经有，直接返回label
				return p.label
			title_simi.append(self.get_title_simi(p, item))
			openTypeList_simi.append(self.get_openTypeList_simi(p, item))
			baseInfoKeyList_simi.append(self.get_baseInfoKeyList_simi(p, item))
			baseInfoValueList_simi.append(self.get_baseInfoValueList_simi(p, item))
			
			mean[0] += title_simi[i]
			mean[1] += openTypeList_simi[i]
			
			mean[2] += baseInfoKeyList_simi[i]
			maxx[2] = max(maxx[2],baseInfoKeyList_simi[i])
			minn[2] = min(minn[2],baseInfoKeyList_simi[i])
			
			mean[3] += baseInfoValueList_simi[i]
			maxx[3] = max(maxx[3],baseInfoValueList_simi[i])
			minn[3] = min(minn[3],baseInfoValueList_simi[i])
			
			i += 1
		
		for i in range(4):
			mean[i] /= len(self.labeled_hudongList)
		
		for p in self.labeled_hudongList: # 计算方差
			var[0] += (title_simi[i]-mean[0])*(title_simi[i]-mean[0])
			var[1] += (openTypeList_simi[i]-mean[1])*(openTypeList_simi[i]-mean[1])
			var[2] += (baseInfoKeyList_simi[i]-mean[2])*(baseInfoKeyList_simi[i]-mean[2])
			var[3] += (baseInfoValueList_simi[i]-mean[3])*(baseInfoValueList_simi[i]-mean[3])
		
		for i in range(4):
			if var[i] ==0.0:
				var[i] = 0.000000001
		
		for i in range(4):
			stand[i] = sqrt(var[i])
		
		# 对于没有openTypeList的 ，赋予平均值
		# 对title和openTypeList进行高斯归一，对后面两项进行maxmin归一
		i = 0	
		for p in self.labeled_hudongList:
			title_simi[i] = (title_simi[i]-mean[0])/stand[0]
			   
			if openTypeList_simi[i] == 0.0: #对于没有出现的，赋予平均值
				openTypeList_simi[i] = mean[1]
			openTypeList_simi[i] = (openTypeList_simi[i]-mean[1])/stand[1]
			
			if baseInfoKeyList_simi[i] == 0.0: #对于没有出现的，赋予平均值
				baseInfoKeyList_simi[i] = mean[2]
			baseInfoKeyList_simi[i] = (baseInfoKeyList_simi[i]-mean[2])/stand[2]
			
			baseInfoValueList_simi[i] = (baseInfoValueList_simi[i]-mean[3])/stand[3]
			
			i+=1
			
		i = 0
		count = 0
		for p in self.labeled_hudongList: # 计算各项相似度的加权和
			s = self.weight[0]*title_simi[i] + self.weight[1]*openTypeList_simi[i] + self.weight[2]*baseInfoKeyList_simi[i] + self.weight[3]*baseInfoValueList_simi[i]
			count += 1
			if count < 2:
				pass
			#	print(str(title_simi[i])+" "+str(openTypeList_simi[i])+" "+str(baseInfoKeyList_simi[i])+" "+str(baseInfoValueList_simi[i]))
			i += 1
			l = p.label
			t = p.title
			curList.append(Node(s,l,t))
		
		curList.sort(key=lambda obj:obj.simi,reverse=True)  # 将训练集按照相对item的相似度进行排序
		
		count = [0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.]	
		for i in range(self.k):
			label = int(curList[i].label)
			count[label] += curList[i].simi
			#print(curList[i].title+"----"+str(curList[i].simi)+'  '+str(label)) # 打印这k个
		
		
		maxx = -233
		answer = 0
		for i in range(17):
			if count[i] > maxx:
				maxx = count[i]
				answer = i
		return answer
	


