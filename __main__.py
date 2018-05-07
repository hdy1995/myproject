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
w2v_path = 'C:\\Users\\Administrator\\PycharmProjects\\untitled2\\test\\word2vec_wx'  # word2vec词向量所在路径
xml_path = 'E:\\大学\\大四\\毕设\\test'  # 遍历路径下所有xml文件

threshold = 0.8  # single-pass聚类的阈值
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

for root, dirs, files in os.walk(xml_path):
    for file in files:
        if file.endswith(".xml"):
            print("%s\%s" % (root, file))

            print('读取xml文件中，请稍候……')
            t1 = time.time()
            text = read_xml("%s\%s" % (root, file))
            t2 = time.time()
            read_xml_time = t2 - t1  # 记录读取xml文件所用时间
            print('读取xml文件完成')
            print('读取xml文件耗时 %.5f 分钟' % (read_xml_time / 60))

            # for n in range(2):  # 测试用
            for n in range(len(text[0]) // 1000):  # 将xml中读取到的内容每1000个进行分块运行single-pass
                print('*******************   ', n, '   *******************')
                Id = text[0][1000 * (n + 0):1000 * (n + 1)]
                Article = text[1][1000 * (n + 0):1000 * (n + 1)]
                Time = text[2][1000 * (n + 0):1000 * (n + 1)]

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
                                               time_list=Time, day=day, top=len(Id)//50)
                t2 = time.time()
                clustering_time = t2 - t1  # 记录聚类所用时间
                print('聚类完成')
                print('聚类耗时 %.5f 分钟' % (clustering_time / 60))

                new_list = clustering.printClusterResult()
                new_id_list.extend(new_list[0])
                new_title_list.extend(new_list[1])
                new_time_list.extend(new_list[2])
                new_vec_list.extend(new_list[3])
                del clustering, new_list

print("========================")
print('SinglePass聚类中，请稍候……')
t1 = time.time()
clustering = SinglePassCluster(threshold=threshold, vector_list=new_vec_list, content_list=new_title_list,
                               id_list=new_id_list, time_list=new_time_list, day=day, top=50)
t2 = time.time()
clustering_time = t2 - t1  # 记录聚类所用时间
print('聚类完成')
print('聚类耗时 %.5f 分钟' % (clustering_time / 60))
clustering.printClusterResult()

t_end = time.time()
cost_time = t_end - t_sta
print("========================")
print('总耗时 %.5f 分钟' % (cost_time / 60))
'''
# 将最终得到结点数最多的20个簇保存下来
output = open('data.pkl', 'wb')
pickle.dump(clustering, output)
output.close()
'''