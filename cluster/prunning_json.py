
file = open('hudong_pedia_1.json', encoding='utf-8')

lines = open('hudong_pedia_1.json',encoding='utf-8').readlines() #打开文件，读入每一行
fp = open('hudong_pedia_2.json','w') #打开你要写得文件pp2.txt
for s in lines:
	fp.write( s.replace(r'\""',r'\"')) # replace是替换，write是写入
fp.close() # 关闭文件