# -*- coding: utf-8 -*-

import time
from myproject.create_vect import create_vect
from myproject.read_dict import read_dict
from myproject.cht_to_chs import cht_to_chs
from myproject.read_xml import read_xml
from myproject.SinglePass import SinglePassCluster
import gensim
import numpy as np

# dict_list = read_dict()  # one-hot模式下
Vect = []
text = []

# word2vec模式下
print('加载模型中，请稍候……')
model = gensim.models.Word2Vec.load('C:/Users/Administrator/PycharmProjects/untitled2/test/word2vec_wx')
Clients_vectors = model.wv.vectors
dict_list = model.wv.index2word
print('加载模型完成')

print('读取xml文件中，请稍候……')
t1 = time.time()
text = read_xml()
t2 = time.time()
read_xml_time = t2 - t1  # 记录读取xml文件所用时间
print('读取xml文件完成')
print('读取xml文件耗时 %.5f 分钟' % (read_xml_time / 60))

# 为了快速得到结果，仅取其中1000条微博测试程序
Id = text[0][10000:12000]
Article = text[1][10000:12000]
Time = text[2][10000:12000]
del text

print('繁体转简体中，清稍候……')
t1 = time.time()
for index in range(len(Article))[1:]:
    Article[index] = cht_to_chs(Article[index])
t2 = time.time()
cht_to_chs_time = t2 - t1  # 记录繁体转简体所用时间
print('繁体转简体完成')
print('繁体转简体耗时 %.5f 分钟' % (cht_to_chs_time / 60))

print('文本分词中，请稍候……')
t1 = time.time()
for article in Article:
    # Vect = Vect + [create_vect(article, dict_list)]  # one-hot模式下
    Vect = Vect + [create_vect(article, dict_list, Clients_vectors)]  # word2vec模式下
t2 = time.time()
create_vect_time = t2 - t1  # 记录文本分词所用时间
print('文本分词完成')
print('文本分词耗时 %.5f 分钟' % (create_vect_time / 60))

print('SinglePass聚类中，请稍候……')
t1 = time.time()
clustering = SinglePassCluster(threshold=0.7, vector_list=Vect, content_list=Article, id_list=Id, time_list=Time)
t2 = time.time()
clustering_time = t2 - t1  # 记录聚类所用时间
print('聚类完成')
print('聚类耗时 %.5f 分钟' % (clustering_time / 60))

print(clustering.printClusterResult())
del clustering
