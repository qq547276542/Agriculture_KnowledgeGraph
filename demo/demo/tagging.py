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
print(sys.path)

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
		collection.delete_many( {'entity1Pos':post.get('entity1Pos') , 'entity1':post.get('entity1') ,'entity2Pos':post.get('entity2Pos'),'entity2':post.get('entity2Pos'),'relation':post.get('relation'),'statement':post.get('statement')})
		return JsonResponse({'code':200})
	else:
		while(True):
			documents_count = collection.count()
			rint = random.randint(0,documents_count-1)
			result = collection.find_one(skip = rint )
			print(result)
			if(len(result) == 7 ):
				return render(request,'taggingSentences.html',{"result": result})