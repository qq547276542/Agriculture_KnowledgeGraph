# coding: utf-8

class HudongItem:
	title = None
	detail = None
	image = None
	openTypeList = None
	baseInfoKeyList = None
	baseInfoValueList = None
	label = None  # label值从文件中读取
	# 初始化，将字典answer赋值给类成员	
	def __init__(self,answer):
		self.title = answer['title']
		self.detail = answer['detail']
		self.image = answer['image']
		self.openTypeList = []
		self.baseInfoKeyList = []
		self.baseInfoValueList = []
		label = -1
		
		if len(answer['openTypeList']) > 0:
			List = answer['openTypeList'].split('##')
			for p in List:
				self.openTypeList.append(p)
	
		if len(answer['baseInfoKeyList']) > 0:
			List = answer['baseInfoKeyList'].split('##')
			for p in List:
				self.baseInfoKeyList.append(p)
		
		if len(answer['baseInfoValueList']) > 0:	
			List = answer['baseInfoValueList'].split('##')
			for p in List:
				self.baseInfoValueList.append(p)
			