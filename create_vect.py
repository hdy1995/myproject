#!/usr/bin/python
# -*- coding: UTF-8 -*-
import numpy as np
import jieba.analyse
from scipy.sparse import csr_matrix

'''
# one-hot模式下
def create_vect(article, dict_list):
    vect = np.zeros(len(dict_list))
    w_sum = 0.000001
    for x, w in jieba.analyse.extract_tags(article, topK=10, withWeight=True):  # 仅取前10个TF-IDF值最大的关键词
        try:
            vect[dict_list.index(x + "\n")] = w  # 构造VSM
            w_sum += w
        except ValueError:
            pass
    vect = vect/w_sum  # 数值归一化方便查看
    # sparse_vect = csr_matrix(vect)  # 转为稀疏矩阵
    return vect
'''


# word2vec模式下
def create_vect(article, dict_list, Clients_vectors):
    vect = np.zeros(256)
    # num = 0
    w_sum = 0.000001
    for x, w in jieba.analyse.extract_tags(article, topK=5, withWeight=True, allowPOS=('n', 'nr', 'ns', 'nt', 'nz')):  # 仅取前10个TF-IDF值最大的关键词
        try:
            vect += Clients_vectors[dict_list.index(x)] * w
            # vect += Clients_vectors[dict_list.index(x)]
            # num += 1
            # vect[dict_list.index(x + "\n")] = w  # 构造VSM
            w_sum += w
        except ValueError:
            pass
            # vect += np.ones(256)
            # w_sum += 1
    # vect = vect / num
    vect = vect / w_sum  # 数值归一化方便查看
    return vect
