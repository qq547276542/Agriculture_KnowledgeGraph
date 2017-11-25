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
		answer = db.matchItembyTitle(title)
		ctx['detail'] = answer['detail']
		ctx['title'] = answer['title']
		imgList = answer['imageList'].split()
		ctx['imgList'] = ""
		for p in imgList:
			ctx['imgList'] += '<img class="card-img-bottom" src="' + str(p) + '" alt="Card image" style="width:25%">'
				
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