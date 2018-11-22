# -*- coding:utf-8 -*-
import fire
import json
import sys
def relation_number():
	#查看图谱中出现的关系，并排序，仅此而已
	relation_dict = {}
	with open('../../wikidataSpider/wikidataProcessing/wikidata_relation.csv','r',encoding='utf8') as fr:
		for line in fr:
			entity_relation = line.split(',')
			if( len(entity_relation) == 3):
				relation = entity_relation[1]
				if relation in relation_dict.keys():
					relation_dict[relation] = relation_dict.get(relation) + 1
				else:
					relation_dict[relation] = 1

		#对关系出现的次数进行排序

		#对字典按照value进行排序
		relation_dict = sorted(relation_dict.items(),key = lambda item:item[1],reverse = True)
		with open("staticResult.txt",'w') as fw:
			for relation in relation_dict :
				fw.write(str(relation)+'\n')

def sentence_relation_number():
#得到train data中各种关系的样本数量
	with open('filter_train_data_all_deduplication.txt', 'r', encoding='utf8') as fr:
		relation_dict = {}
		for line in fr.readlines():
			try:
				item = line.split('\t')[5]
				if relation_dict.get(item) is None:
					relation_dict[item] = 1
				else:
					relation_dict[item] += 1
			except:
				print(line)
		relation_dict = sorted(relation_dict.items(),key = lambda kv:kv[1],reverse=True)
		for key in relation_dict:
			print(key)

#打印包含输入实体的句子
def get_entity_sentence():
	entity = input()
	with open('filtered_data.txt', 'r', encoding='utf8') as fr:
		for line in fr.readlines():
			line_s = line.split('\t')
			if(line_s[1] == entity or line_s[3] == entity):
				print(line)

#打印包含输入关系的句子
def get_relation_sentence():
	relation = input()
	with open('filtered_data.txt', 'r', encoding='utf8') as fr:
		for line in fr.readlines():
			line_s = line.split('\t')
			if (line_s[5].strip() == relation):
				print(line)


#过滤得到包含指定关系的样本，除去实体1和实体2相同的样本，把两个实体都是国家的样本去掉，去掉实体类型为0(invalid),16(Other)的样本
def filter_dataset():
	country_list  = []
	relation_list = ['instance of','has part','subclass of','parent taxon','material used','natural product of taxon']
	entity_type = {}
	with open('entities.txt','r',encoding='utf8')as fr:
		for line in fr.readlines():
			try:
				word,type = line.split()
			except:
				raise IndexError
			entity_type[word] = str(type)



	with open('country-code.json','r',encoding = 'utf8') as fr:
		country_json = json.load(fr)
		for x in country_json:
			country_list.append(x['cn'])

	with open('filter_train_data_all_deduplication.txt','r',encoding = 'utf8') as fr:
		with open('filtered_data.txt','w',encoding='utf8') as fw:
			for line in fr.readlines():
				line_s = line.split('\t')
				#在关系列表中的关系
				if(line_s[5].strip() in relation_list):
					#去掉实体一和实体二相同的句子
					if(line_s[1] == line_s[3]):
						continue
					#去掉实体一和实体二都是国家的句子
					if(line_s[1].strip() in country_list and line_s[3].strip() in country_list):
						continue
					#去掉实体类型为"0"或"16"的样本
					if entity_type[line_s[1].strip()] == '0' or entity_type[line_s[3].strip()] =='0' or \
						entity_type[line_s[1].strip()] == '16' or entity_type[line_s[3].strip()] == '16':
						continue
					fw.write(line)


#得到NA数据
def get_na_entities():
	#目前已经有关系的实体对 , 这里认为，如果A和B有关系，那么B和A也有关系
	entities_has_relation = []
	with open('filtered_data.txt','r',encoding='utf8') as fr:
		for line in fr.readlines():
			line_s = line.split('\t')
			if((line_s[1].strip(),line_s[3].strip()) not in entities_has_relation):
				entities_has_relation.append((line_s[1].strip(),line_s[3].strip()))
				entities_has_relation.append((line_s[3].strip(),line_s[1].strip()))


	#所有实体的列表
	entities_list = []

	with open('entities.txt','r',encoding='utf8') as fr:
		for line in fr.readlines():
			line_s = line.split()
			if(line_s[0].strip() not in entities_list):
				entities_list.append(line_s[0].strip())


	with open('entity2id.json','r',encoding='utf8') as fr:
		entity2id = json.load(fr)

	#得到没有关系的实体对

	cnt = 0
	with open('no_relation_pairs.txt','w',encoding='utf8') as fw:
		for i in range(len(entities_list)):
			print("%s" %format(1.0*i/len(entities_list),'0.2f'),end='',flush=True)
			for j in range(i+1,len(entities_list)):
				id1 = entity2id[entities_list[i]]
				id2 = entity2id[entities_list[j]]
				if( (id1,id2) not in entities_has_relation ):
					cnt += 1
					entities_has_relation.append((id1,id2))
					fw.write(entities_list[i]+"\t"+entities_list[j]+'\n')
				if(cnt%20 ==0):
					i += 1
					break
				if(cnt>500000):
					break
			if(cnt>500000):
				break
#统计同一对实体之间所有关系数量的分布
def entity_relation_number():

	with open('entity2id.json','r',encoding='utf8') as fr:
		entity2id = json.load(fr)

	entity_pair_relation = dict()
	with open('../../wikidataSpider/wikidataProcessing/wikidata_relation.csv', 'r', encoding='utf8') as fr:
		line = fr.readline()
		while(True):
			line = fr.readline()
			if(not line):
				break
			line_s = line.split(',')
			relation = line_s[1].strip()
			if(line_s[0].strip() not in entity2id or line_s[2].strip() not in entity2id):
				continue
			id1 = entity2id[line_s[0].strip()]
			id2 = entity2id[line_s[2].strip()]
			if entity_pair_relation.get((id1,id2)) is None :
				entity_pair_relation[(id1,id2)] = [relation]
			elif relation not in entity_pair_relation[(id1,id2)]:
				entity_pair_relation[(id1,id2)].append(relation)



	with open('../../wikidataSpider/wikidataProcessing/wikidata_relation2.csv','r',encoding='utf8') as fr:
		line = fr.readline()
		while (True):
			line = fr.readline()
			if (not line):
				break
			line_s = line.split(',')
			relation = line_s[1].strip()
			if(line_s[0].strip() not in entity2id or line_s[2].strip() not in entity2id):
				continue
			id1 = entity2id[line_s[0].strip()]
			id2 = entity2id[line_s[2].strip()]
			if entity_pair_relation.get((id1, id2)) is None:
				entity_pair_relation[(id1, id2)] = [relation]
			elif relation not in entity_pair_relation[(id1, id2)]:
				entity_pair_relation[(id1, id2)].append(relation)


	num_dict = {}

	for key in entity_pair_relation:
		num  =  len(entity_pair_relation[key])
		if(num_dict.get(num) is None):
			num_dict[num] = 1
		else:
			num_dict[num] += 1
	print(num_dict)



if __name__ == '__main__':
	fire.Fire()
