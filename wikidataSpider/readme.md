# 说明

> 本项目为一些用于获取知识图谱中三元组关系的python脚本。包括爬取Wikidata数据的爬虫、爬取复旦知识工场数据的爬虫(由于知识工场限制爬取，这部分暂时不好用)、提取所有中文维基页面的脚本以及将Wikidata三元组数据对齐到中文维基页面语句的脚本。

### 运行环境

python3、 Scrapy、neo4j(仅对齐时需要)



> 注意：下面所有爬虫执行命令scrapy crawl XXX 请在各个模块的根目录执行，否则可能由于路径问题找不到文件导致程序报错

 

### wikidataCrawler

**用来爬取wikidata上定义的所有关系**

wikidata中的所有关系都汇总在该网页上[(链接)](https://www.wikidata.org/wiki/Wikidata:List_of_properties/Summary_table) ，wikidataCrawler将该网页下的汇总的所有关系及其对应的中文名称爬取下来，存储为json格式

![](https://raw.githubusercontent.com/CrisJk/SomePicture/master/blog_picture/wikiRelationSumary.png)

##### 使用方法

进入到wikidataCrawler目录下，运行`scrapy crawl relation`即可爬取wikidata中定义的所有关系。可以得到`relation.json`和`chrmention.json`。

* `relation.json`内容: 关系的id，关系所属的大类，关系所属子类，对应的链接，关系的英文表示
* `chrmention.json`内容: 关系的id，关系的中文表示（对于不包含中文表示的数据暂时不做处理）。



将`relation.json`和`chrmention.json`的数据进行合并，运行`mergeChrmentionToRelation.ipynb`即可，得到的结果存储在`result.json`中，匹配失败的存在`fail.json` 中

### wikientities

**用来爬取实体，返回json格式**

进入到wikientities目录下，运行`scrapy crawl entity`。可以得到 `entity.json`。

`entity.json` 是以predict_labels.txt中的实体为搜索词，在wikidata上搜索返回的json内容。

`entity.json`中还包括搜索词(即实体)以及实体所属的类别(和predict_labels.txt中一样)也加入json中存储。

> 由于我目前想做一个农业领域的知识图谱，因此predict_label.txt中很多词都是关于农业的，若想爬取其他实体，则自己修改predict_label.txt中的数据即可。

### wikidataRelation说明

##### 用来爬取实体和实体间的关系三元组，返回三元组

Wikidata是一个开放的全领域的知识库，其中包含大量的实体以及实体间的关系。下图是一个wikidata的实体页面

![](https://raw.githubusercontent.com/CrisJk/SomePicture/master/blog_picture/wikidataPage.png)



从图中可以看到wikidata实体页面包含实体的描述和与该实体相关联的其它实体及对应的关系。

wikidataRelation爬取得到的是实体和实体间的三元关系，例如`合成橡胶`和`石油`之间存在`material used`的关系，因此可以得到如下json格式的三元组：

` {"entity1": "合成橡胶", "relation": "material used", "entity2": "石油"}`

##### 使用方法

首先运行preProcess.py，得到readytoCrawl.json。然后进入到wikidataRelation目录下，运行scrapy crawl entityRelation。可以得到`entityRelation.json` 。

`entityRelation.json`是利用`entity.json`中的所有实体为基础，获取与这些实体相关的其他实体和关系。

### wikidataProcessing 

##### 用来处理得到的三元组关系(entityRelation.json)

将得到的entityRelation.json 处理成csv，并且存入neo4j数据库。该文件夹下的两个文件`hudong_pedia.csv　`和`hudong_pedia2.csv` 是爬取互动百科相关页面得到的，对应的就是wikientities目录下的`predict_label.txt`中的实体。运行`relationDataProcessing.py` 可以得到`new_node.csv` (即从wikidata实体页面中爬取得到的实体不包含在`predict_label.txt`中的部分)、`wikidata_relation.csv`(predict_label.txt中实体之间的关系)以及`wikidata_relation2.csv`(predict_label.txt中实体和新发现实体间的关系)，将该目录下所有csv导入到neo4j中，具体操作参见[Agriculture_KnowledgeGraph](https://github.com/qq547276542/Agriculture_KnowledgeGraph) 中的项目部署部分。

### CN_DBpediaCrawler

CN_DBpedia限制访问，需要向复旦大学知识工场申请API，否则只能限制每分钟爬取次数，这里的爬虫还有些问题，暂时不能使用。

### wikiextractor

wikiextractor是用来获取维基百科语料的工具，维基百科有wiki dump可以直接下载：[下载链接]([http://download.wikipedia.com/zhwiki/latest/zhwiki-latest-pages-articles.xml.bz2](http://download.wikipedia.com/zhwiki/latest/zhwiki-latest-pages-articles.xml.bz2)) ,下载好之后，利用wikiextractor工具进行处理，可以剔除掉一些无用的信息，直接得到维基百科语料库。[wikiextractor工具链接](https://github.com/attardi/wikiextractor) ,下载并安装后，将wiki dump放在wikiextractor目录下，执行命令

```shell
bzcat zhwiki-latest-pages-articles.xml.bz2 | python WikiExtractor.py -b 500K -o extracted -
```

可以得到处理好的维基百科语料，在目录extractor下。



由于得到的语料既有简体也有繁体，所以要进行繁简体转换。将本项目wikiextractor\extracted目录下的三个python文件复制到你处理好的维基百科语料的目录(extractor)下，运行convLan.py便可以将繁体转化为简体。



### TrainDataBaseOnWiki

##### 用于将从wikidata知识库中获取的三元组关系对齐到中文维基的语料库上

首先必须将`wikidataProcessing`目录下的csv导入到neo4j中，才能成功运行。运行`extractTrainingData.py`后，可以得到`train_data.txt` ，其内容包含:

entity1	entity2	statement	relation

得到train_data.txt后，使用dataScrubbing.py处理得到的数据,包括:

* 错误处理

  部分句子有换行，把换行去掉

  第一次产生的数据train_data.txt，由于之前程序在切割字符串时出了问题，因此relation这一列不对，这里重新处理一下

* 选择农业相关的数据

  从所有训练集中挑选出与农业有关的数据

运行
```shell
python dataScrubbing.py handleError
```
执行错误管理模块

运行
```shell
python dataScrubbing.py selectAgriculturalData
```
执行数据选择模块
