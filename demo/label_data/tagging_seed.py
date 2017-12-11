# -*- coding: utf-8 -*-
import json

## 先生成一部分很明显的标签

def read_word():
	file_object = open('word_list.txt','r')
	all_list = []
	for f in file_object:
		all_list.append(f)
	return all_list
	
# 标注不合法数据
def is_num(s):
	flag = True
	for p in s:
		if p>='0' and p<='9':
			pass
		else:
			flag = False
	return flag

def only_num_letter(s):
	flag = True
	for p in s:
		if p>='0' and p<='9':
			pass
		elif p=='零' or p=='一' or p=='二' or p=='三' or p=='四' or p=='五' or p=='六' or p=='七' or p=='八'or p=='九' or p=='十':
			pass
		elif p=='百'or p=='千'or p=='万'or p=='亿':
			pass
		else:
			flag =False
	return flag	
		
def create_invalid():
	all_list = read_word()
	file_object = open('invalid2.txt','w')
#	for word in all_list:
#		word = word.strip() #需要把\n去除
#		if word[len(word)-1] == '年':
#			file_object.write(word+" 0\n")
	for word in all_list:
		word = word.strip()
		if only_num_letter(word):
			file_object.write(word+" 0\n")
	file_object.close()
	
#create_invalid()
	
# 标注人物
def surname_table():
	table = set({'李','王','张','刘','陈','杨','赵','周','吴','徐','孙','胡','朱','何','郭'})
	#李、王、张、刘、陈、杨、赵、黄、周、吴、徐、孙、胡、朱、高、林、何、郭和马
	return table
	
def create_person():  ##最后还是只检查了100个，因为姓名很容易看错
	all_list = read_word()
	file_object = open('person.txt','w')
	surname = surname_table()
	for word in all_list:
		word = word.strip()
		if word[0] in surname and len(word)<=3 :
			file_object.write(word+" 1\n")
	file_object.close()

#create_person()

# 标注地点
def loc_table():
	table = set({'国','市','区','县','省'})
	return table
	
def create_location():  ##只检查了200个
	all_list = read_word()
	file_object = open('location.txt','w')
	loc = loc_table()
	for word in all_list:
		word = word.strip()
		if word[len(word)-1] in loc :
			file_object.write(word+" 2\n")
	file_object.close()

#create_location()

# 标注机构
def is_org(s):
	table = set({'大学','学院','委员会','公司','论坛','大会'})
	if '大学' in s or '学院' in s or '委员会' in s or '公司' in s or '论坛' in s or '大会' in s:
		return True
	return False
	
def create_organization():  ##
	all_list = read_word()
	file_object = open('organization.txt','w')
	for word in all_list:
		word = word.strip()
		if is_org(word) :
			file_object.write(word+" 3\n")
	file_object.close()
	
#create_organization()
	
# 标注政治经济名词
def is_eco(s):
	table = set({'税','经济','条例','补贴','投资'})
	if '税' in s or '经济' in s or '条例' in s or '补贴' in s or '投资' in s or '政策' in s:
		return True
	return False
	
def create_econo():  ##
	all_list = read_word()
	file_object = open('Political_economy.txt','w')
	for word in all_list:
		word = word.strip()
		if is_eco(word) :
			file_object.write(word+" 4\n")
	file_object.close()
	
#create_econo()
	
# 标注动物
def ani_table():
	table = set({'牛','羊','鸡','鸟','狗','犬','虫','鱼','鸭','猫','蛙'})
	return table
	
def create_animal():  ##只检查了200个
	all_list = read_word()
	file_object = open('Animal.txt','w')
	ani = ani_table()
	for word in all_list:
		word = word.strip()
		if word[len(word)-1] in ani :
			file_object.write(word+" 5\n")
	file_object.close()
	
#create_animal()
	
# 标注植物
def plant_table():
	table = set({'草','花','果','桃','菇','麦','米','菜'})
	return table
	
def create_plant():  ##只检查了200个
	all_list = read_word()
	file_object = open('Plant.txt','w')
	plant = plant_table()
	for word in all_list:
		word = word.strip()
		if word[len(word)-1] in plant :
			file_object.write(word+" 6\n")
	file_object.close()
	
#create_plant()
	
# 标注化学物质
def che_table():
	table = set({'剂','肥','盐','油','碳','气','液','氮','氯'})
	return table
	
def create_chemicals():  ##只检查了200个
	all_list = read_word()
	file_object = open('Chemicals.txt','w')
	che = che_table()
	for word in all_list:
		word = word.strip()
		if word[len(word)-1] in che :
			file_object.write(word+" 7\n")
	file_object.close()
	
#create_chemicals()
	
# 标注气候季节
def is_cli(s):
	if '春天' in s or '夏天' in s or '秋天' in s or '冬天' in s or '旱' in s or '雨' in s or '雾' in s or '雪' in s  or '季节' in s:
		return True
	return False
	
def create_climate():  ##
	all_list = read_word()
	file_object = open('Climate.txt','w')
	for word in all_list:
		word = word.strip()
		if is_cli(word) :
			file_object.write(word+" 8\n")
	file_object.close()
	
#create_climate()
	
# 标注动植物产品
def is_food(s):
	if '烤' in s or '煮' in s or '汤' in s or '饼' in s or '米粉' in s or '奶' in s or '面' in s or '酱' in s  or '衣' in s:
		return True
	return False
	
def create_foodItem():  ##
	all_list = read_word()
	file_object = open('foodItem.txt','w')
	for word in all_list:
		word = word.strip()
		if is_food(word) :
			file_object.write(word+" 9\n")
	file_object.close()
	
#create_foodItem()
	
# 标注动植物疾病
def dis_table():
	table = set({'病','症','痛','疼','衰'})
	return table
	
def create_disease():  ##只检查了200个
	all_list = read_word()
	file_object = open('disease.txt','w')
	dis = dis_table()
	for word in all_list:
		word = word.strip()
		if word[len(word)-1] in dis :
			file_object.write(word+" 10\n")
	file_object.close()
	
#create_disease()

# 标注营养素
def is_nut(s):
	if '营养' in s or '维生素' in s or '矿物质' in s or '脂肪' in s or '碳水化合物' in s:
		return True
	return False
	
def create_nutrient():  ##
	all_list = read_word()
	file_object = open('Nutrients.txt','w')
	for word in all_list:
		word = word.strip()
		if is_nut(word) :
			file_object.write(word+" 12\n")
	file_object.close()

#create_nutrient()

# 标注农机具
# 标注动植物疾病
def imple_table():
	table = set({'机','器','备','犁','耙'})
	return table
	
def create_implements():  ##只检查了200个
	all_list = read_word()
	file_object = open('Agricultural_implements.txt','w')
	imple = imple_table()
	for word in all_list:
		word = word.strip()
		if word[len(word)-1] in imple :
			file_object.write(word+" 14\n")
	file_object.close()
	
#create_implements()
	
# 标注农业技术
def is_tech(s):
	if '栽培' in s or '防疫' in s or '嫁接' in s :
		return True
	return False
	
def create_technology():  ##
	all_list = read_word()
	file_object = open('Technology.txt','w')
	for word in all_list:
		word = word.strip()
		if is_tech(word) :
			file_object.write(word+" 15\n")
	file_object.close()
	
create_technology()