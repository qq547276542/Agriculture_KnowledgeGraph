# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators import csrf
from pinyin import pinyin

import sys
sys.path.append("..")
from toolkit.pre_load import tree

# 读取实体解析的文本
def show_overview(request):
	ctx ={}
	if 'node' in request.GET:
		node = request.GET['node']
		fatherList = tree.get_father(node)
		branchList = tree.get_branch(node)
		leafList = tree.get_leaf(node)
		ctx['node'] = "分类专题：["+node+"]"
		
		rownum = 4   #一行的词条数量
		leaf = ""
		
		
		alpha_table = {}
		for alpha in range(ord('A'),ord('Z')+1):
			alpha_table[chr(alpha)] = []
			
		for p in leafList:
			py = pinyin.get_initial(p)
			alpha = ord('A')
			for s in py:
				t = ord(s)
				if t>=ord('a') and t <= ord('z'):
					t = t+ord('A')-ord('a')
				if t>=ord('A') and t <= ord('Z'):
					alpha = t
					break
			alpha_table[chr(alpha)].append(p)
		
		for kk in range(ord('A'),ord('Z')+1):
			k = chr(kk)
			v = alpha_table[k]
			if len(v)==0:
				continue
			add_num = rownum - len(v)%rownum # 填充的数量
			add_num %= rownum
			for i in range(add_num):  # 补充上多余的空位
				v.append('')
			leaf += '<div><span class="label label-warning">&nbsp;&nbsp;'+k+'&nbsp;&nbsp;</span></div><br/>'
			for i in range(len(v)):
				if i%rownum == 0:
					leaf += "<div class='row'>"
				leaf += '<div class="col-md-3">'
				leaf += '<p><a href="detail?title=' + v[i] + '">'
				if len(v[i]) > 10:
					leaf += v[i][:10] + '...'
				else:
					leaf += v[i]
				leaf += '</a></p>'
				leaf += '</div>'
				if i%rownum == rownum-1:
					leaf += "</div>"
			leaf += '<br/>'		
		ctx['leaf'] = leaf
		
		# 父节点列表
		father = '<ul class="nav nav-pills nav-stacked">'
		for p in fatherList:
			father += '<li role="presentation"> <a href="overview?node=' 
			father += p + '">'
			father += '<i class="fa fa-hand-o-right" aria-hidden="true"></i>&nbsp;&nbsp;' + p + '</a></li>'
		father += '</ul>'
		if len(fatherList) == 0:
			father = '<p>已是最高级分类</p>'
		ctx['father'] = father
		
		# 非叶子节点列表
		branch = '<ul class="nav nav-pills nav-stacked">'
		for p in branchList:
			branch += '<li role="presentation"> <a href="overview?node=' 
			branch += p + '">'
			branch += '<i class="fa fa-hand-o-right" aria-hidden="true"></i>&nbsp;&nbsp;' + p + '</a></li>'
		branch += '</ul>'
		if len(branchList) == 0:
			branch = '<p>已是最低级分类</p>'
		ctx['branch'] = branch
		
		# 分类树构建
		level_tree = tree.create_UI(node)
		ctx['level_tree'] = level_tree
		
		
	return render(request, "overview.html", ctx)
	
