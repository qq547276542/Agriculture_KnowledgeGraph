# Agriculture_KnowledgeGraph

------------

### 目录结构：

```
.
├── MyCrawler                 // ---scrapy爬虫项目---
│   ├── MyCrawler
│   │   ├── __init__.py
│   │   ├── data             //爬取数据存放路径
│   │   │   └── agri_economic.json
│   │   ├── items.py         //items对应图谱中的结点
│   │   ├── middlewares.py
│   │   ├── pipelines.py     //过滤管道
│   │   ├── settings.py
│   │   └── spiders          //爬虫脚本存放路径
│   │       ├── __init__.py
│   │       └── agri_pedia.py
│   ├── mySpider.log
│   └── scrapy.cfg
└── demo                       // ---django知识图谱项目---
	├── demo				   // 存放view,用于后台和前端交互
	│   ├── __init__.py
	│   ├── detail_view.py
	│   ├── index_ERform_view.py
	│   ├── index_view.py
	│   ├── settings.py
	│   ├── urls.py
	│   └── wsgi.py
	├── manage.py
	├── neo4jModel             // 自己写的neo4j Model层
	│   ├── __init__.py
	│   └── models.py
	├── static                 // 用于保存静态模板
	│   ├── css
	│   │   └── bootstrap.min.css
	│   └── js
	│       ├── bootstrap.min.js
	│       └── jquery.min.js
	└── templates              // html前端页面
		├── base.html
		├── detail.html
		└── index.html
```

### 项目配置

系统需要安装：

- scrapy     ---爬虫框架
- django     ---web框架
- neo4j       ---图数据库
- thulac      ---分词、词性标注
- py2neo    ---python连接neo4j的工具



## 思路

1.根据19000条农业网词条，按照筛法提取名词（分批进行，每2000条1批，每批维护一个不可重集合）

2.将9批词做交集，生成农业词典1

3.将词典1的词在互动百科中进行爬取，抛弃不存在的页面，提取页面内容，存到数据库中

4.根据页面内容，构造每个词的特征，进行聚类

5.最后提取出农业词语，剔除非农业词语

