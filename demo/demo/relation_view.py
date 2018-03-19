from django.shortcuts import render
from django.http import HttpResponse
from toolkit.pre_load import neo_con
from django.http import JsonResponse
import os

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
			return render(request,'relation.html',{'ctx':json.dumps(ctx,ensure_ascii=False)})
		else:
			#返回查询结果
			#将查询结果按照"关系出现次数"的统计结果进行排序
			relationCountDict = {}
			filePath = os.path.abspath(os.path.join(os.getcwd(),"."))
			with open(filePath+"/toolkit/relationStaticResult.txt","r") as fr:
				for line in fr:
					relationNameCount = line.split(",")
					relationName = relationNameCount[0][2:-1]
					relationCount = relationNameCount[1][1:-2]
					relationCountDict[relationName] = int(relationCount)
			for i in range( len(entityRelation) ):
				relationName = entityRelation[i]['rel']['type']
				relationCount = relationCountDict.get(relationName)
				if(relationCount is None ):
					relationCount = 0
				entityRelation[i]['relationCount'] = relationCount

			entityRelation = sorted(entityRelation,key = lambda item:item['relationCount'],reverse = True)

			return render(request,'relation.html',{'entityRelation':json.dumps(entityRelation,ensure_ascii=False)})

	return render(request,"relation.html",{'ctx':ctx})