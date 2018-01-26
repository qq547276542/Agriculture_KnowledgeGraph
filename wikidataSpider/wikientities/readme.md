# wikientities 说明

### 运行环境

python3、 Scrapy

### 使用说明

进入到该目录下，运行`scrapy crawl enitity`即可爬取wikidata中定义的所有关系。可以得到`entity.json`。

`entity.json` 是以predict_labels.txt中的实体为搜索词，在wikidata上搜索返回的json内容。我将wikidata返回的json数据，我还把搜索词(这个其实wikidata返回的json数据里本身就有，我爬的时候没注意，于是自己手动拼上去了，即entityOriginName)以及实体所属的类别(和predict_labels.txt中一样)也加入json中存储。
