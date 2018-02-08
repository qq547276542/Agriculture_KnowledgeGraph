from django.shortcuts import render
from toolkit.pre_load import neo_con
def search_relation(request):
	ctx = {}
	#根据传入的实体名称搜索出关系
	if request.GET:
		entity = request.GET['user_text']
		#连接数据库
		db = neo_con
		entityRelation = db.getEntityRelationbyEntity(entity)
		if entityRelation is None:
			ctx['title'] = '<h1>数据库中暂未添加该实体</h1>'
			return render(request,"relation.html",ctx)
		else:
			entityRelationDict = dict(entityRelation)
			print(entityRelationDict)
			print(entityRelation)
			return render(request,"relation.html",entityRelationDict)

	return render(request,"relation.html")