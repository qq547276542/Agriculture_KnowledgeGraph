# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.decorators import csrf
from django.http import JsonResponse
import os
import random
import sys
import os
import json
file_path = os.path.abspath(os.path.join(os.getcwd(),".."))
sys.path.append(file_path)

from toolkit.pre_load import collection
from toolkit.pre_load import testDataCollection

def tagging(request):
	if(request.method == "POST"):
		# entity1 = request.POST.get("entity1")
		# entity2 = request.POST.get("entity2")
		# relation = request.POST.get("relation")
		# statement = request.POST.get("statement")
		post = json.loads(request.body)
		post_id = testDataCollection.insert_one(post)
		collection.delete_many( {'Entity1':post.get('entity1') , 'Entity2':post.get('entity2'),'Relation':post.get('relation'),'Statement':post.get('statement')} )
		return JsonResponse({'code':200})
	else:
		while(True):
			documents_count = collection.count()
			rint = random.randint(0,documents_count-1)
			result = collection.find_one(skip = rint )
			if(len(result) == 5 ):

				# #从测试集中选取一个句子和标签
				# filePath = os.path.abspath(os.path.join(os.getcwd(),"../TrainDataBaseOnWiki/finalData/train_data.txt"))
				# statement , entity1 ,entity2 ,relation = statementSelector()

				# #如果标签是对的，则将这个样本写到训练集文件中(已标注)
				# #如果标签是错的，则填写一个正确的标签
				# #如果不知道该如何标注，换一个

				return render(request,'taggingSentences.html',{"result": result})