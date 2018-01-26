import json

with open('entities2.json', 'r') as f:
	for line in f:
		entityjson = json.loads(line)
		print(entityjson)
