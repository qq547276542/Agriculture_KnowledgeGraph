from langconv import *
import os

#获取当前文件路径
filePath = os.path.abspath(os.path.join(os.getcwd(),"."))

for root,dirs,files in os.walk(filePath):
	#得到当前目录下所有文件夹
	for each in dirs:
		#忽略__pycache__下的文件
		if(each == "__pycache__"):
			continue
		#将繁体转化为简体
		for root2,dirs2,files2 in os.walk(filePath+"/"+each):
			for eachFile in files2:
				with open(filePath+"/"+each+"/"+eachFile+"_zh_hans",'w') as fw:
					with open(filePath+"/"+each+"/"+eachFile,'r') as fr:
						for line in fr:
							wikidata = Converter('zh-hans').convert(line)
							fw.write(wikidata+'\n')







