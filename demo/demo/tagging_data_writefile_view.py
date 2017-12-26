# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators import csrf
import sys
import json
import random

sys.path.append("..")
from toolkit.pre_load import pre_load_thu

##  先将标注写入文件，之后跳转到tagging_cache.html再进行新页面的跳转
def tagging_push(request):
	ctx = {}
	# 先将已有的labels存入字典中
	file_object = open('label_data/labels.txt','r')
	s = set()
	for f in file_object:
		pair = f.split()
		s.add(pair[0].strip())
	file_object.close()
	
	file_object = open('label_data/word_list.txt','r')
	all_list = []
	for f in file_object:
		all_list.append(f.strip())
	ln = len(all_list)
	next_title = all_list[random.randint(0,ln)]
	
	if 'label' in request.GET and 'title' in request.GET:
		title = request.GET['title'].strip()
		label = request.GET['label'].strip()
		if label != None:
			file_object = open('label_data/labels.txt','a')
			if title in s:
				print("该title已存在，冲突！")
			else:
				file_object.write(title+" "+label+"\n")
				s.add(title)
			file_object.close()
		else:
			print('用户未选择label')
		
	while next_title in s:  # 如果冲突就再选
		next_title = all_list[random.randint(0,ln)]
		
	ctx['next'] = "<input id='next' value='" + next_title + "' style='display:none;'></input>"
		
			
	return render(request, "tagging_cache.html", ctx)

