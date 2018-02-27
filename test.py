# -*- coding: utf-8 -*-

import time
import numpy as np
from myproject import cluster_unit
from myproject.compute_cosine import cos
from myproject.create_vect import create_vect
from myproject.read_dict import read_dict
from myproject.cht_to_chs import cht_to_chs
from myproject.read_xml import read_xml


class SinglePassCluster:
    def __init__(self, threshold, vector_list, content_list):
        """
        :param t:一趟聚类的阈值
        :param vector_list:
        """
        self.threshold = threshold  # 一趟聚类的阈值
        self.vectors = np.array(vector_list)  # 存储每篇文章的特征向量
        self.content_list = content_list
        self.cluster_list = []  # 聚类后簇的列表
        t1 = time.time()
        self.clustering()
        t2 = time.time()
        self.cluster_num = len(self.cluster_list)  # 聚类完成后  簇的个数
        self.spend_time = t2 - t1  # 一趟聚类花费的时间

    def clustering(self):
        # 初始新建一个簇
        self.cluster_list.append(cluster_unit.ClusterUnit())
        # 读入的第一个文章（结点）归入第一个簇中
        self.cluster_list[0].addNode(0, self.vectors[0], self.content_list[0])
        # 遍历所有的文章  开始进行聚类  index 从1->(len-1)
        for index in range(len(self.vectors))[1:]:
            current_vector = self.vectors[index]
            # 与簇的质心的最小距离
            min_distance = cos(current_vector, self.cluster_list[0].centroid)
            # 最小距离的簇的索引
            min_cluster_index = 0
            for cluster_index, one_cluster in enumerate(self.cluster_list[1:]):
                # enumerate会将数组或列表组成一个索引序列
                # 寻找距离最小的簇，记录下距离和对应的簇的索引
                distance = cos(current_vector, one_cluster.centroid)
                if distance > min_distance:
                    min_distance = distance
                    min_cluster_index = cluster_index + 1
            # 最小距离小于阈值，则归于该簇
            if min_distance > self.threshold:
                self.cluster_list[min_cluster_index].addNode(index, current_vector, self.content_list[index])
            else:
                new_cluster = cluster_unit.ClusterUnit()
                new_cluster.addNode(index, current_vector, self.content_list[index])
                self.cluster_list.append(new_cluster)
                del new_cluster

    def printClusterResult(self, label_dict=None):
        # 打印出聚类结果
        # label_dict:节点对应的标签字典
        print("**********single-pass cluster result******")
        # 对簇列表重新排序，并仅显示节点最多的前20个内容
        print_cluster_list = sorted(self.cluster_list, key=lambda ClusterUnit: ClusterUnit.node_num, reverse=True)[:20]
        for index, one_cluster in enumerate(print_cluster_list):
            print("cluster_index:%s" % index)
            # 簇的结点列表
            print(one_cluster.node_list)
            print(one_cluster.title_list)
            if label_dict is not None:
                # 若有提供标签字典，则输出该簇的标签
                print(" ".join([label_dict[n] for n in one_cluster.node_list]))
                print("node num:%s" % one_cluster.node_num)
                print("========================")
        print("the number of nodes %s" % len(self.vectors))
        print("the number of cluster %s" % self.cluster_num)
        print("spend time %.5fs" % self.spend_time)


if __name__ == '__main__':
    dict_list = read_dict()
    Vect = []
    text = []
    print('读取xml文件中，请稍候……')
    t1 = time.time()
    text = read_xml()
    t2 = time.time()
    read_xml_time = t2 - t1  # 记录读取xml文件所用时间
    print('读取xml文件完成')
    print('读取xml文件耗时 %.5f 分钟' % (read_xml_time/60))
    Article = text[1][:100]  # 为了快速得到结果，仅取前1000条微博测试程序

    print('繁体转简体中，清稍候……')
    t1 = time.time()
    for index in range(len(Article))[1:]:
        Article[index] = cht_to_chs(Article[index])
    t2 = time.time()
    cht_to_chs_time = t2 - t1  # 记录繁体转简体所用时间
    print('繁体转简体完成')
    print('繁体转简体耗时 %.5f 分钟' % (cht_to_chs_time/60))

    print('文本分词中，请稍候……')
    t1 = time.time()
    for article in Article:
        Vect = Vect + [create_vect(article, dict_list)]
    t2 = time.time()
    create_vect_time = t2 - t1  # 记录文本分词所用时间
    print('文本分词完成')
    print('文本分词耗时 %.5f 分钟' % (create_vect_time/60))

    threshold = 0.4
    vector_list = Vect
    content_list = Article

    print('single-pass聚类中，请稍候……')
    t1 = time.time()
    clustering = SinglePassCluster(threshold, vector_list, content_list)
    t2 = time.time()
    clustering_time = t2 - t1  # 记录聚类所用时间
    print('聚类完成')
    print('聚类耗时 %.5f 分钟' % (clustering_time/60))

    print(clustering.printClusterResult())




