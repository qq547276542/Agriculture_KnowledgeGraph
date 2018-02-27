from django.shortcuts import render
from django.http import HttpResponse
from toolkit.pre_load import neo_con
from django.http import JsonResponse

import json
def search_relation(request):
	ctx = {}
	#根据传入的实体名称搜索出关系
	if(request.GET):
		entity = request.GET['user_text']
		#连接数据库
		db = neo_con
		entityRelation = db.getEntityRelationbyEntity(entity)
		if len(entityRelation) == 0:
			#若数据库中无法找到该实体，则返回数据库中无该实体
			ctx= {'title' : '<h1>数据库中暂未添加该实体</h1>'}
			return render(request,'relation.html',{'ctx':json.dumps(ctx)})
		else:
			#返回查询结果
			return render(request,'relation.html',{'entityRelation':json.dumps(entityRelation)})

	return render(request,"relation.html",{'ctx':ctx})