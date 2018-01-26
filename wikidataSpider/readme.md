# 说明

### 运行环境

python3、 Scrapy

### wikidataCrawler使用说明

**用来爬取wikidata上定义的所有关系**

进入到该目录下，运行`scrapy crawl relation`即可爬取wikidata中定义的所有关系。可以得到`relation.json`和`chrmention.json`。

其中`relation.json`中包含关系的id,关系所属的大类，关系所属子类，对应的链接以及关系的英文表示

`chrmention.json`中包含关系的id以及关系的中文表示，对于不包含中文表示的数据暂时不做处理。得到的中文可能是繁体，暂时不做处理。



将`relation.json`和`chrmention.json`的数据进行合并，运行`mergeChrmentionToRelation.ipynb`即可，得到的结果存储在`result.json`中，匹配失败的存在`fail.json` 中

### wikientities使用说明

**用来爬取实体，返回json格式**

进入到该目录下，运行`scrapy crawl enitity`即可爬取wikidata中定义的所有关系。可以得到`entity.json`。

`entity.json` 是以predict_labels.txt中的实体为搜索词，在wikidata上搜索返回的json内容。我将wikidata返回的json数据，我还把搜索词(这个其实wikidata返回的json数据里本身就有，我爬的时候没注意，于是自己手动拼上去了，即entityOriginName)以及实体所属的类别(和predict_labels.txt中一样)也加入json中存储。

