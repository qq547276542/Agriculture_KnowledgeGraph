import json
import thulac
import time
# n
# all+n  (all 不包含 vm)
# a+n
# np 人名
# ns 地名
# ni 机构名
# nz 其它专名
# t和r 时间和代词该步不用加，但是在命名实体识别时需要考虑（这里做个备注）
# i 习语
# j 简称
# x 其它
# 不能含有标点w
	
def nowok(s): #当前词的词性筛选
	
	if s=='n' or s=='np' or s=='ns' or s=='ni' or s=='nz':
		return True
	if s=='i' or s=='j' or s=='x' or s=='id' or s=='g' or s=='t':
		return True
	if s=='t' or s=='m':
		return True
	return False	

def judge(s):  #含有非中文和英文，数字的词丢弃
	num_count = 0
	for ch in s:
		if u'\u4e00' <= ch <= u'\u9fff':
			pass
		elif '0' <= ch <= '9':
			num_count += 1
			pass
		elif 'a' <= ch <= 'z':
			pass
		elif 'A' <= ch <= 'Z':
			pass
		else:
			return False
	if num_count == len(s):  ##如果是纯数字，丢弃
		return False
	return True

# 给定分词结果，提取NER
def createWordList(x):
	i = 0
	n = len(x)
	L = []
	while i < n:
		if judge(x[i][0]) == False :
			i += 1
			continue;
		if nowok(x[i][1]):  
			L.append(x[i][0])
			
		i += 1
		
	return L
			

def createTable(num):
	start = time.time()
	thu = thulac.thulac()
	file = open('agri_economic.json', encoding='utf-8')
	print("begin!")
	f = json.load(file)
	count = 0
	file_text = ""
	for p in f:
		count += 1
		if int(count/100) != num:
			continue
		if count % 10 == 0:
			cur = time.time()
			print("now id : " + str(count) + "  table size :" )
			print("Running Time : " + str(int(cur-start)) + " s......")
		detail = p['detail']
#		if len(detail) > 600:
#			detail = detail[0:600]
		title = p['title']
		# 分词
		text = thu.cut(detail)
		wordList = createWordList(text)
		file_text += title
		for word in wordList:
			file_text += ' ' + word
		file_text += '\n'
				
	file_object = open('article'+str(num)+".txt",'w')
	file_object.write(file_text)
	file_object.close()

createTable(0)
#createTable(1)
#createTable(2)
#createTable(3)
#createTable(4)
#createTable(5)
#createTable(6)
#createTable(7)
#createTable(8)
#createTable(9)

#test()
	
	
#def test():  
#	thu = thulac.thulac()
#	detail = "指在干旱、半干旱地区依靠自然降水栽培小麦。"
#	text = thu.cut(detail)
#	for x in text:
#		print(x[1])
#		

		
		