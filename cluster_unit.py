# -*- coding: utf-8 -*-

import numpy as np
import logging
from myproject.del_day import del_day


# 定义一个簇单元
class ClusterUnit:
    def __init__(self):
        self.node_list = []  # 该簇包含的结点列表
        self.vec_list = []  # 该簇包含的结点特征向量
        self.title_list = []  # 该簇中包含的结点的文本内容
        self.id_list = []  # 该簇中包含的id编号
        self.time_list = []  # 该簇中包含的发布时间
        self.similarity_list = []  # 该簇中包含的结点的相似度
        self.node_num = 0  # 簇中结点个数
        self.centroid = None  # 簇质心
        self.new_title = None  # 当前节点的时间
        self.first_title = None  # 该簇目前最早的时间
        self.last_title = None  # 该簇目前最晚的时间
        self.comments = []  # 该簇目前包含的评论数
        self.reposts = []  # 该簇目前包含的转发数
        self.hot = 0  # 该簇的热度

    def addNode(self, node=0, node_vec=None, title=None, id=None, time=None, comments=0, reposts=0, max_similarity=1):
        """
        为本簇添加指定结点，并更新簇质心
        :param node: 结点
        :param node_vec: 结点特征向量
        :param title: 结点内容
        :param id: 结点编号
        :param time: 结点时间
        :param max_similarity: 结点相似度
        :return:
        """
        self.node_list.append(node)
        self.vec_list.append(node_vec)
        self.title_list.append(title)
        self.id_list.append(id)
        self.time_list.append(time)
        self.similarity_list.append(max_similarity)
        self.new_title = time
        self.comments.append(comments)
        self.reposts.append(reposts)
        try:
            # 更新质心
            self.centroid = (self.node_num * self.centroid + node_vec) / (self.node_num + 1)
            if del_day(self.first_title, self.new_title) > 0:
                self.first_title = self.new_title
            elif del_day(self.last_title, self.new_title) < 0:
                self.last_title = self.new_title
        except TypeError:
            # 初始化质心
            self.centroid = np.array(node_vec)
            self.first_title = self.new_title
            self.last_title = self.new_title
        self.node_num += 1

    def removeNode(self, node=0, node_vec=None, title=None, id=None, time=None, max_similarity=1):
        try:
            self.node_list.remove(node)
            self.title_list.remove(title)
            self.id_list.remove(id)
            self.time_list.remove(time)
            self.similarity_list.remove(max_similarity)
            self.new_title = time
            try:
                self.centroid = (self.node_num * self.centroid - node_vec) / (self.node_num - 1)
            except ZeroDivisionError:
                self.centroid = None
            self.node_num -= 1
        except ValueError:
            # 该结点不在簇中
            raise ValueError("%s not in this cluster" % node)

    def moveNode(self, node, node_vec, title, another_cluster):
        # 移除本簇一个结点，到另一个簇中
        self.removeNode(node=node, node_vec=node_vec, title=title)
        another_cluster.addNode(node=node, node_vec=node_vec, title=title)

    def printNode(self):
        logging.info("簇中结点个数为:%s，簇质心为:%s" % self.node_num, self.centroid)
        logging.info("各个结点如下:\n")
        for title in self.title_list:
            logging.info(title)
