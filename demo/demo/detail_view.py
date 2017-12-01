# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators import csrf
import thulac
 
import sys
sys.path.append("..")
from neo4jModel.models import Neo4j


# 接收GET请求数据
def showdetail(request):
	ctx = {}
	if 'title' in request.GET:
		# 连接数据库
		db = Neo4j()
		db.connectDB()
		title = request.GET['title']
		answer = db.matchHudongItembyTitle(title)
		ctx['detail'] = answer['detail']
		ctx['title'] = answer['title']
		image = answer['image']
		
		ctx['image'] = '<img class="rounded card-img-top img-fluid" src="' + str(image) + '" alt="该条目无图片" style="width:30%" >'
		
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
			text += '<span class="badge badge-success">' + str(p) + '</span> '
		ctx['openTypeList'] = text
		
		text = ""
		keyList = answer['baseInfoKeyList'].split('##')
		valueList = answer['baseInfoValueList'].split('##')
		i = 0
		while i < len(keyList) :
			value = " "
			if i < len(valueList):
				value = valueList[i]
			text += "<tr>"
			text += '<td class="font-weight-bold">' + keyList[i] + '</td>'
			text += '<td>' + value + '</td>'
			i += 1
			
			if i < len(valueList):
				value = valueList[i]
			if i < len(keyList) :
				text += '<td class="font-weight-bold">' + keyList[i] + '</td>'
				text += '<td>' + value + '</td>'
			else :
				text += '<td class="font-weight-bold">' + '</td>'
				text += '<td>' + '</td>'
			i += 1
			text += "</tr>"
		ctx['baseInfoTable'] = text
				
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