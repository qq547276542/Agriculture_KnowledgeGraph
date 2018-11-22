##### 用于将从wikidata知识库中获取的三元组关系对齐到中文维基的语料库上

首先必须将`wikidataProcessing`目录下的csv导入到neo4j中，才能成功运行。运行`extractTrainingData.py`后，可以得到`train_data.txt` ，其内容包含:

entity1pos	entity1	entity2pos	entity2	setence	relation

(注:该文件夹下的parallelTrainingData.py是后来加的，用来得到NA关系的数据，可以参考这个代码来并行得到train_data.txt)

从维基预料中对齐得到的训练集里面有很多属性关系(中文)，甚至还有些关系为空值，把这部分过滤掉，得到**filter_train_data_all.txt**

```shell
python filterRelation.py
```

有些python文件因为文件名变动可能会报错，修改文件名即可

#### 使用步骤

* 1 首先完成wikiextractor中的操作
* 2 将wikidataProcessing目录下的csv导入neo4j中
* 3 运行`extractTrainingData.py` 得到train_data.txt (时间非常漫长，建议改成并行，添加进度条，或者把wikiextractor中数据量减少)
* 4 运行filterRelation.py
* 5 运行deduplication.sh去重，得到**filter_train_data_all_deduplication.txt** ，完成!

#### 各文件说明

* Parallel_extract_training.py: 并行抽取NA的样本
* extractTrainingData.py: 抽取得到train_data.txt
* Deduplication.sh:去掉重复的样本
* filterRelation.py:过滤关系
* dataScrubbing(弃用)


