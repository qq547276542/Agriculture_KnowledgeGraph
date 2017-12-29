# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators import csrf
 
import sys
sys.path.append("..")
from toolkit.pre_load import pre_load_thu,neo_con
from toolkit.NER import get_NE,temporaryok

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

# 读取实体解析的文本
def ER_post(request):
	ctx ={}
	if request.POST:
		key = request.POST['user_text']
		thu1 = pre_load_thu  #提前加载好了
		# 使用thulac进行分词 TagList[i][0]代表第i个词
		# TagList[i][1]代表第i个词的词性
		key = key.strip()
		TagList = thu1.cut(key, text=False)
		text = ""
		NE_List = get_NE(key)  #获取实体列表
		
		for pair in NE_List:   #根据实体列表，显示各个实体
			if pair[1] == 0:
				text += pair[0]
				continue
			if temporaryok(pair[1]):
				text += "<a href='#'  data-original-title='" + get_explain(pair[1]) + "(暂无资料)'  data-placement='top' data-trigger='hover' data-content='"+get_detail_explain(pair[1])+"' class='popovers'>" + pair[0] + "</a>"
				continue
			
			text += "<a href='detail.html?title=" + pair[0] + "'  data-original-title='" + get_explain(pair[1]) + "'  data-placement='top' data-trigger='hover' data-content='"+get_detail_explain(pair[1])+"' class='popovers'>" + pair[0] + "</a>"
		
		ctx['rlt'] = text
			
#		while i < length:
#			# 尝试将2个词组合，若不是NE则组合一个，还不是就直接打印文本
#			p1 = TagList[i][0]
#			p2 = "*-"  # 保证p2没被赋值时，p1+p2必不存在
#			if i+1 < length:
#				p2 = TagList[i+1][0]
#				
#			t1 = TagList[i][1]
#			t2 = "*-"
#			if i+1 < length:
#				t2 = TagList[i+1][1]
#			
#			p = p1 + p2
#			if i+1 < length and preok(t1) and nowok(t2):
#				answer = db.matchHudongItembyTitle(p)
#				if answer != None:
#					text += "<a href='detail.html?title=" + str(p) + "' data-toggle='tooltip' title='" + get_explain(t2) + "'>" + p + "</a>"
#					i += 2
#					continue
#			
#			p = p1
#			if nowok(t1):
#				answer = db.matchHudongItembyTitle(p)
#				if answer != None:
#					text += "<a href='detail.html?title=" + str(p) + "' data-toggle='tooltip' title='" + get_explain(t1) + "'>" + p + "</a>"
#					i += 1
#					continue
#				elif temporaryok(t1):
#					text += "<a href='#' data-toggle='tooltip' title='" + get_explain(t1) + "(暂无资料)'>" + p + "</a>"
#					i += 1
#					continue
#					
#					
#			i += 1
#			text += str(p)
				
		seg_word = ""
		length = len(TagList)
		for t in TagList:   #测试打印词性序列
			seg_word += t[0]+" <strong><small>["+t[1]+"]</small></strong> "
		seg_word += ""
		ctx['seg_word'] = seg_word
		
	return render(request, "index.html", ctx)
	
