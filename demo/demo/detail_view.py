# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators import csrf
import thulac
 
import sys
sys.path.append("..")
from toolkit.pre_load import neo_con
from toolkit.pre_load import wv_model


# 接收GET请求数据
def showdetail(request):
	ctx = {}
	if 'title' in request.GET:
		# 连接数据库
		db = neo_con
		
		title = request.GET['title']
		answer = db.matchHudongItembyTitle(title)
		ctx['detail'] = answer['detail']
		ctx['title'] = answer['title']
		image = answer['image']
		
		ctx['image'] = '<img src="' + str(image) + '" alt="该条目无图片" height="100%" width="100%" >'
		
		ctx['baseInfoKeyList'] = []
		List = answer['baseInfoKeyList'].split('##')
		for p in List:
			ctx['baseInfoKeyList'].append(p)
			
		ctx['baseInfoValueList'] = []
		List = answer['baseInfoValueList'].split('##')
		for p in List:
			ctx['baseInfoValueList'].append(p)
			
		text = ""
		List = answer['openTypeList'].split('##')
		for p in List:
			text += '<span class="badge bg-important">' + str(p) + '</span> '
		ctx['openTypeList'] = text
		
		text = '<table class="table table-striped table-advance table-hover"> <tbody>'
		keyList = answer['baseInfoKeyList'].split('##')
		valueList = answer['baseInfoValueList'].split('##')
		i = 0
		while i < len(keyList) :
			value = " "
			if i < len(valueList):
				value = valueList[i]
			text += "<tr>"
			text += '<td><strong>' + keyList[i] + '</strong></td>'
			text += '<td>' + value + '</td>'
			i += 1
			
			if i < len(valueList):
				value = valueList[i]
			if i < len(keyList) :
				text += '<td><strong>' + keyList[i] + '</strong></td>'
				text += '<td>' + value + '</td>'
			else :
				text += '<td><strong>' + '</strong></td>'
				text += '<td>' + '</td>'
			i += 1
			text += "</tr>"
		text += " </tbody> </table>"
		if answer['baseInfoKeyList'].strip() == '':
			text = ''
		ctx['baseInfoTable'] = text 
		
		tagcloud = ""
		taglist = wv_model.get_simi_top(answer['title'], 10)
		for tag in taglist:
			tagcloud += '<a href= "./detail.html?title=' + str(tag) + '"> '
			tagcloud += str(tag) + "</a>"
			print(tag)
		ctx['tagcloud'] = tagcloud
				
	return render(request, "detail.html", ctx)
	
#	
## -*- coding: utf-8 -*-
#from django.http import HttpResponse
#from django.shortcuts import render_to_response
#import thulac
# 
#import sys
#sys.path.append("..")
#from neo4jModel.models import Neo4j
#
#def search_detail(request):
#	return render_to_response('detail.html')
#
## 接收GET请求数据
#def showdetail(request):
#	request.encoding = 'utf-8'
#	if 'title' in request.GET:
#		# 连接数据库
#		db = Neo4j()
#		db.connectDB()
#		title = request.GET['title']
#		answer = db.matchItembyTitle(title)
#		message = answer['detail']
#				
#	return HttpResponse(message)