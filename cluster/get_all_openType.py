import json

def get_openType():
	file = open('hudong_pedia_1.json', encoding='utf-8')
	table = set()
	f = json.load(file)
	for p in f:
		openTypeList = p['openTypeList']
		openTypeList = openTypeList.split('##')
		for s in openTypeList:
			table.add(s)
			
	print(table)
	print(len(table))
	
get_openType()