# -*- coding:utf-8 -*-

import json
import os
import numpy as np
import random
import config
import jieba
import re


class file_data_loader:
    def __next__(self):
        raise NotImplementedError

    def next(self):
        return self.__next__()

    def next_batch(self, batch_size):
        raise NotImplementedError


class cmp():
    def __init__(self, x):
        self.x = x

    def __lt__(self, other):
        a_key = self.x['head']['id'] + '#' + self.x['tail']['id'] + '#' + self.x['relation']
        b_key = other.x['head']['id'] + '#' + other.x['tail']['id'] + '#' + other.x['relation']

        if (a_key > b_key):
            return False
        elif (a_key == b_key):
            return True
        else:
            return True


class json_file_data_loader(file_data_loader):
    # 以instance作为最小单位
    MODE_INSTANCE = 0
    # 以bag为最小单位，每个bag中实体对相同，一般用于test(因为不知道relation)
    MODE_ENTPAIR_BAG = 1
    # 以bag为最小单位，每个bag中实体对和关系相同，一般用于train
    MODE_RELFACT_BAG = 2

    # chinese word segmentation
    def sentence_segmentation(self, sentence, entity1, entity2):
        jieba.add_word(entity1, freq=999999)
        jieba.add_word(entity2, freq=999999)

        seglist = list(jieba.cut(sentence, cut_all=False, HMM=False))
        jieba.del_word(entity1)
        jieba.del_word(entity2)
        return seglist

    def _load_processed_file(self):
        # train or test
        name_prefix = '.'.join(self.file_name.split('/')[-1].split('.')[:-1])
        word_vec_name_prefix = '.'.join(self.word_vec_file_name.split('/')[-1].split('.')[:-1])
        processed_data_dir = '_processed_data'

        if not os.path.isdir(processed_data_dir):
            return False

        word_npy_file_name = os.path.join(processed_data_dir, name_prefix + '_word.npy')
        pos1_npy_file_name = os.path.join(processed_data_dir, name_prefix + '_pos1.npy')
        pos2_npy_file_name = os.path.join(processed_data_dir, name_prefix + '_pos2.npy')
        rel_npy_file_name = os.path.join(processed_data_dir, name_prefix + '_rel.npy')
        mask_npy_file_name = os.path.join(processed_data_dir, name_prefix + '_mask.npy')
        length_npy_file_name = os.path.join(processed_data_dir, name_prefix + '_length.npy')
        entpair2scope_file_name = os.path.join(processed_data_dir, name_prefix + '_entpair2scope.json')
        relfact2scope_file_name = os.path.join(processed_data_dir, name_prefix + '_relfact2scope.json')
        word_vec_mat_file_name = os.path.join(processed_data_dir, word_vec_name_prefix + '_mat.npy')
        word2id_file_name = os.path.join(processed_data_dir, word_vec_name_prefix + '_word2id.json')

        if not os.path.exists(word_npy_file_name) or \
                not os.path.exists(pos1_npy_file_name) or \
                not os.path.exists(pos2_npy_file_name) or \
                not os.path.exists(rel_npy_file_name) or \
                not os.path.exists(mask_npy_file_name) or \
                not os.path.exists(length_npy_file_name) or \
                not os.path.exists(entpair2scope_file_name) or \
                not os.path.exists(relfact2scope_file_name) or \
                not os.path.exists(word_vec_mat_file_name) or \
                not os.path.exists(word2id_file_name):
            return False

        print("Loading pre-processing files...")
        self.data_word = np.load(word_npy_file_name)
        self.data_pos1 = np.load(pos1_npy_file_name)
        self.data_pos2 = np.load(pos2_npy_file_name)
        self.data_rel = np.load(rel_npy_file_name)
        self.data_mask = np.load(mask_npy_file_name)
        self.data_length = np.load(length_npy_file_name)
        with open(entpair2scope_file_name, 'r', encoding='utf8') as fr:
            self.entpair2scope = json.load(fr)
        with open(relfact2scope_file_name, 'r', encoding='utf8') as fr:
            self.relfact2scope = json.load(fr)
        self.word_vec_mat = np.load(word_vec_mat_file_name)
        with open(word2id_file_name, 'r', encoding='utf8') as fr:
            self.word2id = json.load(fr)

        if (self.data_word.shape[1] != config.model.max_length):
            print("Pre-processing ata is expired, Reprocessing")
            return False
        print('Finish loading')
        return True

    def __init__(self, file_name, word_vec_file_name, rel2id_file_name, mode, shuffle,
                 max_length=config.model.max_length, batch_size=config.model.batch_size):
        '''

        :param file_name: 数据路径
        :param word_vec_file_name: 词向量路径
        :param rel2id_file_name: relation to id 路径
        :param mode: 组织数据的模式,有3种方式:MODE_INSTANCE , MODE_ENTPAIR_BAG,MODE_RELFACT_BAG
        :param shuffle: 是否shuffle数据
        :param max_length: 规定句子的最长长度
        :param batch_size: 定义batch_size
        '''

        self.file_name = file_name
        self.word_vec_file_name = word_vec_file_name
        self.rel2id_file_name = rel2id_file_name
        self.mode = mode
        self.shuffle = shuffle
        self.max_length = max_length
        self.batch_size = batch_size
        with open(rel2id_file_name, 'r') as fr:
            self.rel2id = json.load(fr)

        if (not self._load_processed_file()):
            if file_name is None or not os.path.isfile(file_name):
                raise Exception("[ERROR] Data file doesn't exist")
            if word_vec_file_name is None or not os.path.isfile(word_vec_file_name):
                raise Exception("[ERROR] word2vec file doesn't exist")
            if rel2id_file_name is None or not os.path.isfile(rel2id_file_name):
                raise Exception("[ERROR] word2vec file doesn't exist")

            # load file
            print("Loading data file...")
            with open(self.file_name, 'r', encoding='utf8') as fr:
                self.ori_data = json.load(fr)
            print("Finish loading")

            print("Loading word vector file...")
            with open(self.word_vec_file_name, 'r', encoding='utf8') as fr:
                self.ori_word_vec = json.load(fr)
            print("Finish loading")

            # sort data by entities and relations
            print("sort data")

            self.ori_data.sort(key=cmp)
            print('Finish sorting')

            # pre-processing word vec

            self.word2id = {}
            self.word_vec_tot = len(self.ori_word_vec)
            UNK = self.word_vec_tot
            BLANK = self.word_vec_tot + 1
            self.word2id['UNK'] = UNK
            self.word2id['BLANK'] = BLANK
            self.word_vec_dim = len(self.ori_word_vec[0]['vec'])
            print("Got {} words of {} dims".format(self.word_vec_tot, self.word_vec_dim))
            print("Building word vector matrix and mapping...")

            self.word_vec_mat = np.zeros((self.word_vec_tot, self.word_vec_dim), dtype=np.float32)
            for cur_id, word in enumerate(self.ori_word_vec):
                w = word['word']
                self.word2id[w] = cur_id
                self.word_vec_mat[cur_id, :] = word['vec']

            self.word2id['UNK'] = UNK
            self.word2id['BLANK'] = BLANK

            print("Finish building")

            # Pre-processing
            print("Pre-processing data...")
            self.instance_tot = len(self.ori_data)
            self.entpair2scope = {}  # (head,tail) -> scope
            self.relfact2scope = {}  # (head,tail,rel) -> scope
            self.data_word = np.zeros((self.instance_tot, self.max_length), dtype=np.int32)
            self.data_pos1 = np.zeros((self.instance_tot, self.max_length), dtype=np.int32)
            self.data_pos2 = np.zeros((self.instance_tot, self.max_length), dtype=np.int32)
            self.data_rel = np.zeros((self.instance_tot), dtype=np.int32)
            self.data_mask = np.zeros((self.instance_tot, self.max_length), dtype=np.int32)
            self.data_length = np.zeros((self.instance_tot), dtype=np.int32)

            last_entpair = ''
            last_entpair_pos = -1
            last_relfact = ''
            last_relfact_pos = -1

            dirty_data_number = 0

            pattern = re.compile(r'\s')
            for i in range(self.instance_tot):
                ins = self.ori_data[i]
                dataset = file_name.split("/")[-2]
                if dataset == 'agriculture':
                    ins['sentence'] = re.sub(pattern, '_', ins['sentence'])
                if (ins['relation'] in self.rel2id):
                    self.data_rel[i] = self.rel2id[ins['relation']]
                else:
                    self.data_rel[i] = self.rel2id['NA']

                if dataset == 'nyt':
                    sentence = ' '.join(ins['sentence'].split())
                elif dataset == 'agriculture':
                    sentence = ' '.join(
                        self.sentence_segmentation(ins['sentence'], ins['head']['word'], ins['tail']['word']))
                else:
                    raise NameError
                head = ins['head']['word']
                tail = ins['tail']['word']
                cur_entpair = ins['head']['id'] + '#' + ins['tail']['id']
                cur_relfact = ins['head']['id'] + '#' + ins['tail']['id'] + '#' + ins['relation']

                if (cur_entpair != last_entpair):
                    if (last_entpair != ''):
                        self.entpair2scope[last_entpair] = [last_entpair_pos, i]
                    last_entpair = cur_entpair
                    last_entpair_pos = i

                if (cur_relfact != last_relfact):
                    if (last_relfact != ''):
                        self.relfact2scope[last_relfact] = [last_relfact_pos, i]
                    last_relfact = cur_relfact
                    last_relfact_pos = i

                # position
                if dataset == 'nyt':
                    p1 = sentence.find(' ' + head + ' ')
                    p2 = sentence.find(' ' + tail + ' ')
                    # 如果是首 尾
                    if (p1 == -1):
                        if (sentence[:len(head) + 1] == head + " "):
                            p1 = 0
                        elif (sentence[-len(head) - 1:] == " " + head):
                            p1 = len(sentence) - len(head)
                        else:
                            p1 = 0
                    else:
                        p1 += 1

                    if (p2 == -1):
                        if (sentence[:len(head) + 1] == head + " "):
                            p2 = 0
                        elif (sentence[-len(head) - 1:] == " " + head):
                            p2 = len(sentence) - len(head)
                        else:
                            p2 = 0
                    else:
                        p2 += 1

                elif dataset == 'agriculture':
                    p1 = int(ins['head']['pos'])
                    p2 = int(ins['tail']['pos'])

                words = sentence.split()

                cur_ref_data_word = self.data_word[i]
                cur_pos = 0
                pos1 = -1
                pos2 = -1

                for j, word in enumerate(words):
                    if (j < max_length):
                        if word in self.word2id:
                            cur_ref_data_word[j] = self.word2id[word]
                        else:
                            cur_ref_data_word[j] = UNK
                    if cur_pos == p1:
                        pos1 = j
                        p1 = -1
                    if cur_pos == p2:
                        pos2 = j
                        p2 = -1
                    if dataset == 'nyt':
                        cur_pos += len(word) + 1
                    elif dataset == 'agriculture':
                        tmp = cur_pos
                        cur_pos += len(word)
                        while cur_pos < len(ins['sentence']) and ins['sentence'][cur_pos] == " ":
                            cur_pos += 1
                        if tmp < p1 and cur_pos > p1:
                            pos1 = j
                            p1 = -1

                        if tmp < p2 and cur_pos > p2:
                            pos2 = j
                            p2 = -1
                    else:
                        raise NameError
                if cur_pos == p1:
                    pos1 = len(words) - 1
                if cur_pos == p2:
                    pos2 = len(words) - 1

                if pos1 >= max_length:
                    pos1 = max_length - 1
                if pos2 >= max_length:
                    pos2 = max_length - 1

                for k in range(len(words), max_length):
                    cur_ref_data_word[k] = BLANK

                self.data_length[i] = min(len(words), max_length)

                if (pos1 == -1 or pos2 == -1):
                    print(p1, p2)
                    raise Exception(
                        "[ERROR] Position error, index = {}, sentence = {}, head = {}, tail = {}".format(i, sentence,
                                                                                                         head, tail))

                pos1 = min(pos1, max_length - 1)
                pos2 = min(pos2, max_length - 1)

                pos_min = min(pos1, pos2)
                pos_max = max(pos1, pos2)

                for j in range(max_length):
                    self.data_pos1[i][j] = j - pos1 + max_length
                    self.data_pos2[i][j] = j - pos2 + max_length

                    if (j >= self.data_length[i]):
                        self.data_mask[i][j] = 0
                    elif j <= pos_min:
                        self.data_mask[i][j] = 1
                    elif j <= pos_max:
                        self.data_mask[i][j] = 2
                    else:
                        self.data_mask[i][j] = 3

            if last_entpair != '':
                self.entpair2scope[last_entpair] = [last_entpair_pos, self.instance_tot]

            if last_relfact != '':
                self.relfact2scope[last_relfact] = [last_relfact_pos, self.instance_tot]

            print("Finish pre-processing")

            print("Storing preprocessing file...")
            # train or test
            name_prefix = '.'.join(self.file_name.split('/')[-1].split('.')[:-1])
            word_vec_name_prefix = '.'.join(self.word_vec_file_name.split('/')[-1].split('.')[:-1])
            processed_data_dir = '_processed_data'

            if not os.path.isdir(processed_data_dir):
                os.mkdir(processed_data_dir)

            print("discards data number ", dirty_data_number)
            np.save(os.path.join(processed_data_dir, name_prefix + '_word.npy'), self.data_word)
            np.save(os.path.join(processed_data_dir, name_prefix + '_pos1.npy'), self.data_pos1)
            np.save(os.path.join(processed_data_dir, name_prefix + '_pos2.npy'), self.data_pos2)
            np.save(os.path.join(processed_data_dir, name_prefix + '_rel.npy'), self.data_rel)
            np.save(os.path.join(processed_data_dir, name_prefix + '_mask.npy'), self.data_mask)
            np.save(os.path.join(processed_data_dir, name_prefix + '_length.npy'), self.data_length)
            with open(os.path.join(processed_data_dir, name_prefix + '_entpair2scope.json'), 'w',
                      encoding='utf8') as fw:
                json.dump(self.entpair2scope, fw, ensure_ascii=False)
            with open(os.path.join(processed_data_dir, name_prefix + '_relfact2scope.json'), 'w',
                      encoding='utf8') as fw:
                json.dump(self.relfact2scope, fw, ensure_ascii=False)

            np.save(os.path.join(processed_data_dir, word_vec_name_prefix + '_mat.npy'), self.word_vec_mat)
            with open(os.path.join(processed_data_dir, word_vec_name_prefix + '_word2id.json'), 'w',
                      encoding='utf8') as fw:
                json.dump(self.word2id, fw, ensure_ascii=False)

            print("Finish storing")

        self.instance_tot = self.data_word.shape[0]
        self.entpair_tot = len(self.entpair2scope)
        self.relfact_tot = 0  # relfact数， 除了 relation 关系

        for key in self.relfact2scope:
            if (key[-2:] != 'NA'):
                self.relfact_tot += 1

        self.rel_tot = len(self.rel2id)

        if self.mode == self.MODE_INSTANCE:
            self.order = list(range(self.instance_tot))
        elif self.mode == self.MODE_ENTPAIR_BAG:
            self.order = list(range(len(self.entpair2scope)))
            self.scope_name = []
            self.scope = []
            for key, value in self.entpair2scope.items():
                self.scope_name.append(key)
                self.scope.append(value)
        elif self.mode == self.MODE_RELFACT_BAG:
            self.order = list(range(len(self.relfact2scope)))
            self.scope_name = []
            self.scope = []
            for key, value in self.relfact2scope.items():
                self.scope_name.append(key)
                self.scope.append(value)
        else:
            raise Exception("[ERROR] Invalid mode")

        print("len order", len(self.order))
        self.idx = 0
        if (self.shuffle):
            random.shuffle(self.order)

        print("Total relation fact:%d" % (self.relfact_tot))
        print("Total instance:%d" % (self.instance_tot))

    def __iter__(self):
        return self

    def __next__(self):
        return self.next_batch(self.batch_size)

    def next_batch(self, batch_size):
        if self.idx >= len(self.order):
            self.idx = 0
            if self.shuffle:
                random.shuffle(self.order)
            raise StopIteration

        batch_data = {}

        if self.mode == self.MODE_INSTANCE:
            idx0 = self.idx
            idx1 = self.idx + batch_size

            self.idx = idx1
            batch_data['word'] = self.data_word[idx0:idx1]
            batch_data['pos1'] = self.data_pos1[idx0:idx1]
            batch_data['pos2'] = self.data_pos2[idx0:idx1]
            batch_data['rel'] = self.data_rel[idx0:idx1]
            batch_data['mask'] = self.data_mask[idx0:idx1]
            batch_data['length'] = self.data_length[idx0:idx1]
            batch_data['scope'] = np.stack([list(range(batch_size)), list(range(1, batch_size + 1))], axis=1)
            if idx1 - idx0 < batch_size:
                padding = batch_size - (idx1 - idx0)
                batch_data['word'] = np.concatenate(
                    [batch_data['word'], np.zeros((padding, self.data_word.shape[-1]), dtype=np.int32)])
                batch_data['pos1'] = np.concatenate(
                    [batch_data['pos1'], np.zeros((padding, self.data_pos1.shape[-1]), dtype=np.int32)])
                batch_data['pos2'] = np.concatenate(
                    [batch_data['pos2'], np.zeros((padding, self.data_pos2.shape[-1]), dtype=np.int32)])
                batch_data['mask'] = np.concatenate(
                    [batch_data['mask'], np.zeros((padding, self.data_mask.shape[-1]), dtype=np.int32)])
                batch_data['rel'] = np.concatenate([batch_data['rel'], np.zeros((padding), dtype=np.int32)])
                batch_data['length'] = np.concatenate([batch_data['length'], np.zeros((padding), dtype=np.int32)])

        elif self.mode == self.MODE_ENTPAIR_BAG or self.mode == self.MODE_RELFACT_BAG:
            idx0 = self.idx
            idx1 = self.idx + batch_size

            if idx1 > len(self.order):
                idx1 = len(self.order)

            self.idx = idx1
            _word = []
            _pos1 = []
            _pos2 = []
            _mask = []
            _rel = []
            _ins_rel = []
            _multi_rel = []
            _entpair = []
            _length = []
            _scope = []
            cur_pos = 0
            for i in range(idx0, idx1):
                _word.append(self.data_word[self.scope[self.order[i]][0]:self.scope[self.order[i]][1]])
                _pos1.append(self.data_pos1[self.scope[self.order[i]][0]:self.scope[self.order[i]][1]])
                _pos2.append(self.data_pos2[self.scope[self.order[i]][0]:self.scope[self.order[i]][1]])
                _mask.append(self.data_mask[self.scope[self.order[i]][0]:self.scope[self.order[i]][1]])
                _rel.append(self.data_rel[self.scope[self.order[i]][0]])
                _ins_rel.append(self.data_rel[self.scope[self.order[i]][0]:self.scope[self.order[i]][1]])
                _length.append(self.data_length[self.scope[self.order[i]][0]:self.scope[self.order[i]][1]])
                bag_size = self.scope[self.order[i]][1] - self.scope[self.order[i]][0]
                _scope.append([cur_pos, cur_pos + bag_size])
                cur_pos = cur_pos + bag_size
                if self.mode == self.MODE_ENTPAIR_BAG:
                    _one_multi_rel = np.zeros((self.rel_tot), dtype=np.int32)
                    for j in range(self.scope[self.order[i]][0], self.scope[self.order[i]][1]):
                        _one_multi_rel[self.data_rel[j]] = 1
                    _multi_rel.append(_one_multi_rel)
                    _entpair.append(self.scope_name[self.order[i]])
            for i in range(batch_size - (idx1 - idx0)):
                _word.append(np.zeros((1, self.data_word.shape[-1]), dtype=np.int32))
                _pos1.append(np.zeros((1, self.data_pos1.shape[-1]), dtype=np.int32))
                _pos2.append(np.zeros((1, self.data_pos2.shape[-1]), dtype=np.int32))
                _mask.append(np.zeros((1, self.data_mask.shape[-1]), dtype=np.int32))
                _rel.append(0)
                _ins_rel.append(np.zeros((1), dtype=np.int32))
                _length.append(np.zeros((1), dtype=np.int32))
                _scope.append([cur_pos, cur_pos + 1])
                cur_pos += 1
                if self.mode == self.MODE_ENTPAIR_BAG:
                    _multi_rel.append(np.zeros((self.rel_tot), dtype=np.int32))
                    _entpair.append('None#None')
            batch_data['word'] = np.concatenate(_word)
            batch_data['pos1'] = np.concatenate(_pos1)
            batch_data['pos2'] = np.concatenate(_pos2)
            batch_data['mask'] = np.concatenate(_mask)
            batch_data['rel'] = np.stack(_rel)
            batch_data['ins_rel'] = np.concatenate(_ins_rel)
            if self.mode == self.MODE_ENTPAIR_BAG:
                batch_data['multi_rel'] = np.stack(_multi_rel)
                batch_data['entpair'] = _entpair
            batch_data['length'] = np.concatenate(_length)
            batch_data['scope'] = np.stack(_scope)

        return batch_data

















