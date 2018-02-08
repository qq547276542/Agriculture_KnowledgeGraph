from py2neo import Graph,Node,Relationship

class Neo4j():
	graph = None
	def __init__(self):
		print("create neo4j class ...")
		
	def connectDB(self):
		self.graph = Graph("http://localhost:7474", username="neo4j", password="8313178")
		
	def matchItembyTitle(self,value):
		answer = self.graph.find_one(label="Item",property_key="title",property_value=value)
		return answer

	# 根据title值返回互动百科item
	def matchHudongItembyTitle(self,value):
		answer = self.graph.find_one(label="HudongItem",property_key="title",property_value=value)
		return answer

	# 根据entity的名称返回关系
	def getEntityRelationbyEntity(self,value):
		#TODO 
		answer = self.graph.data("MATCH (entity1) - [rel] -> (entity2)  WHERE entity1.title = \"" +value +"\" RETURN rel,entity2")
		return answer
