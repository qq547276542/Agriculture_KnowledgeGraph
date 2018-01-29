import random

class TREE :
	edge = None  # 层次树邻接表
	leaf = None  # 记录叶子节点
	root = '农业'  # 树的根结点
	curpath = None  # 路径栈
	anspath = None  # 返回路径结果
	
	def read_edge(self, src):
		self.edge = {}  # 层次树邻接表
		vis = set()  # 去重
		with open(src,'r') as f:
			for line in f.readlines():
				if line in vis:
					continue
				vis.add(line)
				cur = line.strip().split(' ')
				u = str(cur[0])
				v = str(cur[1])
				if u not in self.edge:
					self.edge[u] = []
				self.edge[u].append(v)
				
	def read_leaf(self, src):
		self.leaf = {}  # 记录叶子节点
		vis = set()   # 去重
		with open(src,'r') as f:
			for line in f.readlines():
				if line in vis:
					continue
				vis.add(line)
				cur = line.strip().split(' ')
				u = str(cur[0])
				v = str(cur[1])
				if u not in self.leaf:
					self.leaf[u] = []
				self.leaf[u].append(v)
			
	def DFS(self, word, u):
		#print(u)
		self.curpath.append(u)
		if u not in self.leaf or word not in self.leaf[u]: # 如果叶节点儿子中没有目标
			pass
		else:  #返回路径
			path = []
			for p in self.curpath:
				path.append(p)
			path.append(word)
			self.anspath.append(path)  # 把该路径加入答案
			
		if u not in self.edge: #儿子只有叶节点了
			pass
		else: # 递归儿子
			for v in self.edge[u]:
				self.DFS(word, v)
		self.curpath.pop()
				
	def get_path(self, word, unique):  # 可能存在多条路径，所以返回二维数组[路径数][路径]
		self.anspath = []            #unique 为true 代表筛选路径，去除过多重复的路径
		self.curpath = []
		self.DFS(word, self.root)
		random.shuffle(self.anspath)
		if unique == True :
			for i in range(len(self.anspath)):
				j = i + 1
				while j < len(self.anspath):
					seti = set(self.anspath[i])
					setj = set(self.anspath[j])
					unum = len(seti & setj)
					if unum > 2:
						del self.anspath[j]
					else:
						j += 1
		return self.anspath
		
		
# 读取农业层次树
#tree = TREE()
#tree.read_edge('micropedia_tree.txt')
#tree.read_leaf('leaf_list.txt')
#print(tree.get_path('香蕉',True))

		
		
		
				