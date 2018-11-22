## 关系自动抽取

农业知识图谱关系抽取

### data

处理数据集，得到关系抽取需要用到的json文件

步骤:
* 如果当前文件夹下没有`filter_train_data_all_deduplication.txt`, 那么进入wikidataSpider目录，根据TrainDataBaseOnWiki/readme.md中所述方法，获得`filter_train_data_all_deduplication.txt` (生成数据时间比较长，建议用公开数据集测试。使用公开数据集，直接从进入Algorithm,忽略之后所有的操作)
* 运行`python dosomething.py filter_dataset` 得到`filtered_data.txt` 
* 运行`python preprocessing.py rel2id` 得到rel2id.json
* 运行`python preprocessing.py dataset.json`得到dataset.json
* 运行`python preprocessing.py word2vecjson` 得到word2vec.json
* 运行`python preprocessing.py entity2id`得到entity2id.json
* 运行`python preprocessing.py dataset_split`得到train_dataset.json和test_dataset.json



得到的rel2id.json,word2vec.json,entity2id.json,train_dataset.json和test_dataset.json为关系提取算法所需的数据，将其放在algorithm的data/agriculture目录下

### algorithm

关系提取的算法部分,tensorflow实现,代码框架以及PCNN的实现参照https://github.com/thunlp/OpenNRE

##### data

存放关系提取所需的数据，如果只是测试关系提取算法，建议使用nyt等公开数据。

* agriculture 农业知识图谱数据
* nyt 公开数据集，纽约时报数据





