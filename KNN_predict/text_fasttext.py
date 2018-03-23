# coding: utf-8
from pyfasttext import FastText

def text():
	model = FastText('wiki.zh.bin')
	print('load over..')
	s1 = '启航'
	s2 = '董启航'
	s3 = ' 董启文'
	print(model.nearest_neighbors('桃', k=5))
		
#text()