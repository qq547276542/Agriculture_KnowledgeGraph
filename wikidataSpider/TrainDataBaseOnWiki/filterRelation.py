# -*- coding: utf-8 -*-

import os
import sys

#从维基预料中对齐得到的训练集里面有很多属性关系(中文)，甚至还有些关系为空值，把这部分过滤掉

with open('train_data_all.txt','r',encoding='utf8') as fr:
	with open('filter_train_data_all.txt','w',encoding = 'utf8') as fw:
		for line in fr.readlines():
			line_s = line.split('\t')
			if(len(line_s) !=6):
				continue
			elif( (line_s[5][0]>'Z' or line_s[5][0]<'A') and (line_s[5][0]>'z' or line_s[5][0]<'a') ):
				continue
			else:
				fw.write(line)
