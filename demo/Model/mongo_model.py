import sys
import os

import pymongo
from pymongo import MongoClient

class Mongo():
	clent = None
	db = None
	collection = None
	def makeConnection(self):
		self.client = MongoClient('localhost',27017)

	def getDatabase(self,dbName):
		self.db = self.client[dbName]
		return self.db

	def getCollection(self,collectionName):
		self.collection = self.db[collectionName]
		return self.collection

