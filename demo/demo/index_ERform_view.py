# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators import csrf
 
import sys
sys.path.append("..")
from neo4jModel.models import Neo4j
from pre_load import pre_load_thu

def get_explain(s):
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
	return '非实体'
		
def preok(s):  #上一个词的词性筛选
	
	if s=='n' or s=='np' or s=='ns' or s=='ni' or s=='nz':
		return True
	if s=='a' or s=='i' or s=='j' or s=='x' or s=='id' or s=='g' or s=='u':
		return True
	if s=='t' or s=='m':
		return True
	return False
	
def nowok(s): #当前词的词性筛选
	
	if s=='n' or s=='np' or s=='ns' or s=='ni' or s=='nz':
		return True
	if s=='i' or s=='j' or s=='x' or s=='id' or s=='g' or s=='t':
		return True
	if s=='t' or s=='m':
		return True
	return False	
	
def temporaryok(s):  # 一些暂时确定是名词短语的（数据库中可以没有）
	if s=='np' or s=='ns' or s=='ni' or s=='nz':
		return True
	if s=='i' or s=='j' or s=='x' or s=='id':
		return True
	return False

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
		db = Neo4j()
		db.connectDB()
		text = ""
		seg_word = ""
		i = 0
		length = len(TagList)
		for t in TagList:   #测试打印词性序列
			seg_word += t[0]+"_"+t[1]+"  "
		while i < length:
			# 尝试将2个词组合，若不是NE则组合一个，还不是就直接打印文本
			p1 = TagList[i][0]
			p2 = "*-"  # 保证p2没被赋值时，p1+p2必不存在
			if i+1 < length:
				p2 = TagList[i+1][0]
				
			t1 = TagList[i][1]
			t2 = "*-"
			if i+1 < length:
				t2 = TagList[i+1][1]
			
			p = p1 + p2
			if i+1 < length and preok(t1) and nowok(t2):
				answer = db.matchHudongItembyTitle(p)
				if answer != None:
					text += "<a href='detail.html?title=" + str(p) + "' data-toggle='tooltip' title='" + get_explain(t2) + "'>" + p + "</a>"
					i += 2
					continue
			
			p = p1
			if nowok(t1):
				answer = db.matchHudongItembyTitle(p)
				if answer != None:
					text += "<a href='detail.html?title=" + str(p) + "' data-toggle='tooltip' title='" + get_explain(t1) + "'>" + p + "</a>"
					i += 1
					continue
				elif temporaryok(t1):
					text += "<a href='#' data-toggle='tooltip' title='" + get_explain(t1) + "(暂无资料)'>" + p + "</a>"
					i += 1
					continue
					
					
			i += 1
			text += str(p)
				
		ctx['rlt'] = text
		ctx['seg_word'] = seg_word
		
	return render(request, "index.html", ctx)
	
