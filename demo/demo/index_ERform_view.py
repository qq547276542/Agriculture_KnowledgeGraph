# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators import csrf
 
import sys
sys.path.append("..")
from toolkit.pre_load import pre_load_thu,neo_con,predict_labels
from toolkit.NER import get_NE,temporaryok,get_explain,get_detail_explain

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
	
