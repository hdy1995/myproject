# -*- coding: utf-8 -*-

import time
import numpy as np
from myproject import cluster_unit
from myproject.compute_cosine import cos
from myproject.del_day import del_day


class SinglePassCluster:
    def __init__(self, threshold, vector_list, content_list, id_list, time_list):
        """
        :param t:一趟聚类的阈值
        :param vector_list:
        """
        self.threshold = threshold  # 一趟聚类的阈值
        self.vectors = np.array(vector_list)  # 存储每篇文章的特征向量
        self.content_list = content_list  # 存储每篇文章的内容
        self.id_list = id_list  # 存储每篇文章的序号
        self.time_list = time_list  # 存储每篇文章的时间
        self.cluster_list = []  # 聚类后簇的列表
        t1 = time.time()
        self.clustering()  # 聚类操作并统计聚类耗时
        t2 = time.time()
        self.cluster_num = len(self.cluster_list)  # 聚类完成后  簇的个数
        self.spend_time = t2 - t1  # 一趟聚类花费的时间

    def clustering(self):
        # 初始新建一个簇
        self.cluster_list.append(cluster_unit.ClusterUnit())
        # 读入的第一个文章（结点）归入第一个簇中
        self.cluster_list[0].addNode(0, self.vectors[0], self.content_list[0], self.id_list[0], self.time_list[0])
        # 遍历所有的文章  开始进行聚类  index 从1->(len-1)
        for index in range(len(self.vectors))[1:]:
            if index % 100 == 0:
                print(index)
                # print(self.id_list[index])
                # print(self.time_list[index])
            current_vector = self.vectors[index]
            # 与簇的质心的最大相似度
            distance = abs(del_day(self.time_list[0], self.cluster_list[0].first_title) + del_day(self.time_list[0],
                                                                                                  self.cluster_list[
                                                                                                      0].last_title)) / 2
            max_similarity = cos(current_vector, self.cluster_list[0].centroid) - distance * 0.01
            # 最大相似度的簇的索引
            max_cluster_index = 0

            for cluster_index, one_cluster in enumerate(self.cluster_list[1:]):
                # enumerate会将数组或列表组成一个索引序列
                # 寻找相似度最大的簇，记录下距离和对应的簇的索引
                distance = abs(del_day(self.time_list[index], one_cluster.first_title) + del_day(self.time_list[index],
                                                                                                 one_cluster.last_title)) / 2
                similarity = cos(current_vector, one_cluster.centroid) - distance * 0.01
                if similarity > max_similarity:
                    max_similarity = similarity
                    max_cluster_index = cluster_index + 1
            # 最大相似度大于阈值，则归于该簇
            if max_similarity > self.threshold:
                self.cluster_list[max_cluster_index].addNode(index, current_vector, self.content_list[index],
                                                             self.id_list[index], self.time_list[index], max_similarity)
            else:
                new_cluster = cluster_unit.ClusterUnit()
                new_cluster.addNode(index, current_vector, self.content_list[index], self.id_list[index],
                                    self.time_list[index])
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
            print("簇中结点个数为:%s" % one_cluster.node_num)
            # 簇的结点列表
            print(one_cluster.id_list)
            print(one_cluster.title_list)
            print(one_cluster.time_list)
            print(one_cluster.similarity_list)
            print(one_cluster.first_title, one_cluster.last_title)
            print('\n')
            if label_dict is not None:
                # 若有提供标签字典，则输出该簇的标签
                print(" ".join([label_dict[n] for n in one_cluster.node_list]))
                print("node num:%s" % one_cluster.node_num)
                print("========================")
        print("the number of nodes %s" % len(self.vectors))
        print("the number of cluster %s" % self.cluster_num)
        print("spend time %.5fs" % self.spend_time)
