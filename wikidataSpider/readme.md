# 说明

### 运行环境

python3、 Scrapy

### wikidataCrawler说明

**用来爬取wikidata上定义的所有关系**

wikidata中的所有关系都汇总在该网页上[(链接)](https://www.wikidata.org/wiki/Wikidata:List_of_properties/Summary_table) ，wikidataCrawler将该网页下的汇总的所有关系及其对应的中文名称爬取下来，存储为json格式

![](https://raw.githubusercontent.com/CrisJk/SomePicture/master/blog_picture/wikiRelationSumary.png)

##### 使用方法

进入到wikidataCrawler目录下，运行`scrapy crawl relation`即可爬取wikidata中定义的所有关系。可以得到`relation.json`和`chrmention.json`。

其中`relation.json`中包含关系的id,关系所属的大类，关系所属子类，对应的链接以及关系的英文表示

`chrmention.json`中包含关系的id以及关系的中文表示，对于不包含中文表示的数据暂时不做处理。得到的中文可能是繁体，暂时不做处理。



将`relation.json`和`chrmention.json`的数据进行合并，运行`mergeChrmentionToRelation.ipynb`即可，得到的结果存储在`result.json`中，匹配失败的存在`fail.json` 中

### wikientities说明

**用来爬取实体，返回json格式**

进入到wikientities目录下，运行`scrapy crawl entity`。可以得到 `entity.json`。

`entity.json` 是以predict_labels.txt中的实体为搜索词，在wikidata上搜索返回的json内容。我将wikidata返回的json数据，我还把搜索词(这个其实wikidata返回的json数据里本身就有，我爬的时候没注意，于是自己手动拼上去了，即entityOriginName)以及实体所属的类别(和predict_labels.txt中一样)也加入json中存储。

### wikidataRelation说明

##### 用来爬取实体和实体间的关系三元组，返回三元组

wikidataRelation爬取得到的是实体和实体间的三元关系，wikidata中的每一个实体对应的页面包含很多与它有关系的实体，通过爬取这些页面可以得到实体间的关系。例如`合成橡胶`和`石油`之间存在`material used`的关系，因此可以得到如下json格式的三元组：

` {"entity1": "合成橡胶", "relation": "material used", "entity2": "石油"}`

##### 使用方法

进入到wikidataRelation目录下，运行scrapy crawl entityRelation。可以得到`entityRelation.json` 。

`entityRelation.json`是利用`entity.json`中的所有实体为基础，获取与这些实体相关的其他实体和关系。