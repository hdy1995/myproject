#!/usr/bin/python
# -*- coding: UTF-8 -*-
import numpy as np
import jieba.analyse


def create_vect(article, dict_list):
    vect = np.zeros(len(dict_list))
    w_sum = 0.0000000001
    for x, w in jieba.analyse.extract_tags(article, topK=10, withWeight=True):
        try:
            vect[dict_list.index(x + "\n")] = w
            w_sum += w
            # 　print(dict_list.index(x + "\n"), x, w/w_sum)
        except ValueError:
            pass
    vect = vect/w_sum
    # print("-------------")
    return vect
