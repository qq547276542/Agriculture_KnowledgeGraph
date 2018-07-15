# coding: utf-8
import configparser

from py2neo import Graph,Node,Relationship
from hudong_class import HudongItem

class Neo4j():
	graph = None
	def __init__(self):
		print("create neo4j class ...")
		
	def connectDB(self):
		conf = configparser.ConfigParser()
		conf.read('demo/neo4jconfig')
		url = conf.get("neo4jdb", "url")
		username = conf.get("neo4jdb", "username")
		password = conf.get("neo4jdb", "password")
		self.graph = Graph(url, username=username, password=password)
		# self.graph = Graph("http://localhost:7474", username="neo4j", password="abc123")
		print('connect successed')
		
	def matchItembyTitle(self,value):
		answer = self.graph.find_one(label="Item",property_key="title",property_value=value)
		return answer

	# 根据title值返回互动百科item
	def matchHudongItembyTitle(self,value):
		answer = self.graph.find_one(label="HudongItem",property_key="title",property_value=value)
		return answer
			
	# 返回限定个数的互动百科item
	def getAllHudongItem(self, limitnum):
		List = []
		ge = self.graph.find(label="HudongItem", limit=limitnum)
		for g in ge:
			List.append(HudongItem(g))
			
		print('load AllHudongItem over ...')
		return List
		
		
#test = Neo4j()
#test.connectDB()
#a = test.getLabeledHudongItem('labels.txt')
#print(a[10].openTypeList)