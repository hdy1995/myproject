# -*- coding: utf-8 -*-

import numpy as np
import logging


# 定义一个簇单元
class ClusterUnit:
    def __init__(self):
        self.node_list = []  # 该簇包含的结点列表
        self.title_list = []  # 该簇中包含的结点的文本内容
        self.id_list = []  # 该簇中包含的id编号
        self.time_list = []  # 该簇中包含的发布时间
        self.node_num = 0  # 簇中结点个数
        self.centroid = None  # 簇质心

    def addNode(self, node=0, node_vec=None, title=None, id=None, time=None):
        """
        为本簇添加指定结点，并更新簇质心
        :param node: 结点
        :param node_vec: 结点特征向量
        :return:
        """
        self.node_list.append(node)
        self.title_list.append(title)
        self.id_list.append(id)
        self.time_list.append(time)
        try:
            # 更新质心
            self.centroid = (self.node_num * self.centroid + node_vec) / (self.node_num + 1)
        except TypeError:
            # 初始化质心
            self.centroid = np.array(node_vec) * 1
        self.node_num += 1

    def removeNode(self, node=0, node_vec=None, title=None, id=None, time=None):
        try:
            self.node_list.remove(node)
            self.title_list.remove(title)
            self.id_list.remove(id)
            self.time_list.remove(time)
            try:
                self.centroid = (self.node_num * self.centroid - node_vec) / (self.node_num - 1)
            except ZeroDivisionError:
                self.centroid = None
            self.node_num -= 1
        except ValueError:
            # 该结点不在簇中
            raise ValueError("%s not in this cluster" % node)

    def moveNode(self, node, node_vec, title, id, time, another_cluster):
        # 移除本簇一个结点，到另一个簇中
        self.removeNode(node=node, node_vec=node_vec, title=title, id=id, time=time)
        another_cluster.addNode(node=node, node_vec=node_vec, title=title, id=id, time=time)

    def printNode(self):
        logging.info("簇中结点个数为:%s，簇质心为:%s" % self.node_num, self.centroid)
        logging.info("各个结点如下:\n")
        for title in self.title_list:
            logging.info(title)
