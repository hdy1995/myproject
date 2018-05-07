#!/usr/bin/python
# -*- coding: UTF-8 -*-
import numpy as np
import jieba.analyse


# word2vec模式下
def create_vect(article, dict_list, Clients_vectors):
    vect = np.zeros(256)
    w_sum = 0.000001
    jieba.analyse.set_stop_words('stopword.txt')
    for x, w in jieba.analyse.extract_tags(article, topK=3, withWeight=True,
                                           allowPOS=('an', 'vn', 'n', 'nr', 'ns', 'nt', 'nz')):  # 仅取前10个TF-IDF值最大的关键词
        try:
            vect += Clients_vectors[dict_list.index(x)] * w
            w_sum += w
        except ValueError:
            pass
    vect = vect / w_sum  # 数值归一化方便查看
    return vect
