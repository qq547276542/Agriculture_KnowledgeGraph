# -*- coding: utf-8 -*-  
# 根据非叶结点，对叶节点进行爬取
import urllib.request  
from urllib.parse import quote,unquote
import re

pre_str = 'http://fenlei.baike.com/'
root_str = '农业'
def getHtml(url):  
	url = quote(url, safe='/:?=')  # url处理中文
	page = urllib.request.urlopen(url)  
	html = page.read().decode(encoding='utf-8',errors='strict')  
	return html  
	
	
def crawl_page(u_str):
	u_str = u_str.strip()
	print('entry: '+u_str)
	url = pre_str + u_str + r'/list'
	html = getHtml(url)
	s = html.find('link_blue line-25 zoom')
	if s == -1:
		return
	sublist = []   ## 得到了所有子概念名称的列表  
	for i in range(s,999999):
		if html[i]== '/' and html[i-1]=='i' and html[i-2]=='k' and html[i-3]=='i' and html[i-4]=='w':
			i += 1
			j = i
			while html[j]!=r'"' and html[j+1]!='>':
				j += 1
			str = ''
			while i<j:
				str += html[i]
				i += 1
				
			str = unquote(str)
			sublist.append(str)
		
		if html[i]=='<' and html[i+1]=='/' and html[i+2]=='d' and html[i+3]=='l':
			break
	
	for sub in sublist:
		if ' ' in sub:
			continue
		if '+' in sub:
			continue	
		
		sub2 = ""
		for s in sub:  ##把[xxx]去掉，与之前一致
			if s == '[':
				break
			sub2 += s
			
		with open('leaf_list.txt','a') as f:
			f.write(u_str+' '+sub2+"\n")
	 
#flag = 0
with open('treenode_list.txt','r') as f:
	for line in f.readlines():
#		if line.strip() == '农民':
#			flag = 1
#		if flag == 0 :
#			continue
		crawl_page(line)
	
	