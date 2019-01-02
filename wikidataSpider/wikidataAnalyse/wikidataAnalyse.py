relation_dict = {}
with open('wikidata_relation.csv','r') as fr:
	for line in fr:
		entity_relation = line.split(',')
		if( len(entity_relation) == 3):
			relation = entity_relation[1] 
			if relation in relation_dict.keys():
				relation_dict[relation] = relation_dict.get(relation) + 1
			else:
				relation_dict[relation] = 0

	#对关系出现的次数进行排序

	#对字典按照value进行排序
	relation_dict = sorted(relation_dict.items(),key = lambda item:item[1],reverse = True)
	with open("staticResult.txt",'w') as fw:
		for relation in relation_dict :
			fw.write(str(relation)+'\n')