# -*- coding: utf-8 -*-  
# 将leaf_list.txt进行保留第二列，去重，判断是否在neo4j中已存在
import urllib.request  
from urllib.parse import quote,unquote
import re
from neo_models import Neo4j
	
def main():
	neo = Neo4j()
	neo.connectDB()
	s = {}
	with open('leaf_list.txt','r') as f:
		for line in f.readlines():
			itemname = line.split(' ')[1].strip()
			if neo.matchHudongItembyTitle(itemname) != None:
				continue
			if itemname in s:
				continue;
			s[itemname] = 1
			with open('crawled_leaf_list.txt','a') as f:
				f.write(itemname+'\n')		
			
	
main()