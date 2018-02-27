#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re


def read_dict():
    with open("dict.txt", 'r', encoding='UTF-8') as f:
        word_dict = f.readlines()
        # 读取dict.txt

        for i, val in enumerate(word_dict):
            word_dict[i] = re.sub(r' .*$', "", val, re.M)

        # word_dict = sorted(set(word_dict))
        # 将dict.txt重新排序（可省略）
    return word_dict

