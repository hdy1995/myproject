# -*- coding: utf-8 -*-

import time
from myproject.create_vect import create_vect
from myproject.cht_to_chs import cht_to_chs
from myproject.read_xml import read_xml
from myproject.SinglePass import SinglePassCluster
import gensim
import pickle
import os

t_sta = time.time()
text = []

new_id_list = []
new_title_list = []
new_time_list = []
new_vec_list = []
new_comments = []
new_reposts = []
w2v_path = 'C:\\Users\\Administrator\\PycharmProjects\\untitled2\\test\\word2vec_wx'  # word2vec词向量所在路径
xml_path = 'E:\\大学\\大四\\毕设\\test'  # 遍历路径下所有xml文件

threshold = 0.75  # single-pass聚类的阈值
day = 20  # 一个舆情持续的时间

# word2vec模式下
print('加载模型中，请稍候……')
t1 = time.time()
model = gensim.models.Word2Vec.load(w2v_path)
Clients_vectors = model.wv.vectors
dict_list = model.wv.index2word
t2 = time.time()
model_time = t2 - t1  # 记录加载模型所用时间
print('加载模型完成')
print('加载模型耗时 %.5f 分钟' % (model_time / 60))

text = []
f = open('newtest.txt', 'r', encoding='utf-8')
line = f.readline()
while line:
    text.append(line)
    line = f.readline()
f.close()

Article = text
Id = range(len(Article))
Time = [0]*len(Article)
Comments = [0]*len(Article)
Reposts = [0]*len(Article)

print('繁体转简体中，清稍候……')
t1 = time.time()
for index in range(len(Article))[1:]:
    # print(Article[index])
    Article[index] = cht_to_chs(Article[index])
    # print(Article[index])
t2 = time.time()
cht_to_chs_time = t2 - t1  # 记录繁体转简体所用时间
print('繁体转简体完成')
print('繁体转简体耗时 %.5f 分钟' % (cht_to_chs_time / 60))

print('文本分词中，请稍候……')
Vect = []
t1 = time.time()
for article in Article:
    Vect = Vect + [create_vect(article, dict_list, Clients_vectors)]  # word2vec模式下
t2 = time.time()
create_vect_time = t2 - t1  # 记录文本分词所用时间
print('文本分词完成')
print('文本分词耗时 %.5f 分钟' % (create_vect_time / 60))

print('SinglePass聚类中，请稍候……')
t1 = time.time()
clustering = SinglePassCluster(threshold=threshold, vector_list=Vect, content_list=Article, id_list=Id,
                               time_list=Time, day=day, comments=Comments, reposts=Reposts, top=20)
t2 = time.time()
clustering_time = t2 - t1  # 记录聚类所用时间
print('聚类完成')
print('聚类耗时 %.5f 分钟' % (clustering_time / 60))

clustering.printClusterResult()

t_end = time.time()
cost_time = t_end - t_sta
print("========================")
print('总耗时 %.5f 分钟' % (cost_time / 60))

