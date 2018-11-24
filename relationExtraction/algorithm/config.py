import os
import sys
import tensorflow as tf
# 以instance作为最小单位
MODE_INSTANCE = 0
# 以bag为最小单位，每个bag中实体对相同，一般用于test(因为不知道relation)
MODE_ENTPAIR_BAG = 1
# 以bag为最小单位，每个bag中实体对和关系相同，一般用于train
MODE_RELFACT_BAG = 2

root_path = os.getcwd()
print(root_path)
class dir:
    dataset_dir = {
        "nyt": {
            "root":os.path.join(root_path,"data/nyt/"),
            "train":os.path.join(root_path,"data/nyt/train.json"),
            "test":os.path.join(root_path,"data/nyt/test.json"),
            "rel2id":os.path.join(root_path,"data/nyt/rel2id.json"),
            "word2vec":os.path.join(root_path,"data/nyt/word_vec.json")
        },
        'agriculture': {
            "root":os.path.join(root_path,"data/agriculture/"),
            "train":os.path.join(root_path,"data/agriculture/train_dataset.json"),
            "test":os.path.join(root_path,"data/agriculture/test_dataset.json"),
            "rel2id":os.path.join(root_path,"data/agriculture/rel2id.json"),
            "word2vec":os.path.join(root_path,"data/agriculture/word2vec.json"),
            "entity2id":os.path.join(root_path,"data/agriculture/entity2id.json")
        }
    }

class model:
    #super parameter

    #句子最长长度
    max_length = 60
    batch_size  = 16


    train_level  = MODE_RELFACT_BAG
    test_level =  MODE_ENTPAIR_BAG

    encoder = "pcnn"

    max_epoch = 60


    learning_rate= 0.05
    optimizer = tf.train.AdamOptimizer

    pos_embedding_dim = 5

    pcnn_kernel_size = 3
    pcnn_hidden_size = 230
    pcnn_stride_size = 1
    pcnn_activation = tf.nn.relu

    gpu_list = [0]

    test_epoch = 1 #训练时，(epoch + 1)%test_epoch == 0 时测试一次查看精度