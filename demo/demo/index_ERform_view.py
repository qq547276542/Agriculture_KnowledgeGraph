# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators import csrf
import thulac
 
import sys
sys.path.append("..")
from neo4jModel.models import Neo4j

# 读取实体解析的文本
def ER_post(request):
	ctx ={}
	if request.POST:
		key = request.POST['q']
		thu1 = thulac.thulac()  #默认模式
		# 使用thulac进行分词 TagList[i][0]代表第i个词
		# TagList[i][1]代表第i个词的词性
		TagList = thu1.cut(key, text=False) 
		db = Neo4j()
		db.connectDB()
		text = ""
		i = 0
		length = len(TagList)
		while i < length:
			# 尝试将3个词组合，若不是NE则组合两个，还不是NE则组合一个，还不是就直接打印文本
			p1 = TagList[i][0]
			p2 = "*-"  # 保证p2和p3没被赋值时，p1+p2+p3必不存在
			p3 = "*-"
			if i+1 < length:
				p2 = TagList[i+1][0]
			if i+2 < length:
				p3 = TagList[i+2][0]
				
			p = p1 + p2 + p3
			answer = db.matchItembyTitle(p)
			if answer != None:
				text += "<a href='detail.html?title=" + str(p) + "'>" + p + "</a>"
				i += 3
				continue
			
			p = p1 + p2
			answer = db.matchItembyTitle(p)
			if answer != None:
				text += "<a href='detail.html?title=" + str(p) + "'>" + p + "</a>"
				i += 2
				continue
			
			p = p1
			answer = db.matchItembyTitle(p)
			if answer != None:
				text += "<a href='detail.html?title=" + str(p) + "'>" + p + "</a>"
				i += 1
				continue
			i += 1
			
			text += str(p)
				
		ctx['rlt'] = text
		
	return render(request, "index.html", ctx)
	
