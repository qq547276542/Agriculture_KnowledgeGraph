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
		return r'机构\会议'
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
		
	if s == 'n':
		return '名词实体'
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
				text += "<a href='#' data-toggle='tooltip' title='" + get_explain(pair[1]) + "(暂无资料)'>" + pair[0] + "</a>"
				continue
			text += "<a href='detail.html?title=" + pair[0] + "' data-toggle='tooltip' title='" + get_explain(pair[1]) + "'>" + pair[0] + "</a>"
		
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
			seg_word += t[0]+"_"+t[1]+"  "
			
		ctx['seg_word'] = seg_word
		
	return render(request, "index.html", ctx)
	
