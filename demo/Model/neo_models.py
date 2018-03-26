from py2neo import Graph,Node,Relationship
import configparser

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
		
	def matchItembyTitle(self,value):
		answer = self.graph.find_one(label="Item",property_key="title",property_value=value)
		return answer

	# 根据title值返回互动百科item
	def matchHudongItembyTitle(self,value):
		answer = self.graph.find_one(label="HudongItem",property_key="title",property_value=value)
		return answer

	# 根据entity的名称返回关系
	def getEntityRelationbyEntity(self,value):
		answer = self.graph.data("MATCH (entity1) - [rel] -> (entity2)  WHERE entity1.title = \"" +value +"\" RETURN rel,entity2")
		return answer
