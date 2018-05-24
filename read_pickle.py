import pickle
import jieba.analyse
from collections import Counter
import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

#  读取保存的簇
pkl_file = open('test5.pkl', 'rb')
new_data = pickle.load(pkl_file)
pkl_file.close()
new_data.top = 1  # 修改显示的簇数量
# new_data.printClusterResult()

print_cluster_list = sorted(new_data.cluster_list, key=lambda ClusterUnit: ClusterUnit.node_num, reverse=True)[
                     :new_data.top]
# print_cluster_list = sorted(new_data.cluster_list, key=lambda ClusterUnit: ClusterUnit.hot, reverse=True)[:new_data.top]

# f = open('1.txt', "w+", encoding="utf8")
for index, one_cluster in enumerate(print_cluster_list):
    print("cluster_index:%s" % index)
    print("簇中结点个数为:%s" % one_cluster.node_num)
    texts = "".join(one_cluster.title_list)  # 重新提取该簇的关键词
    keywords = jieba.analyse.extract_tags(texts, topK=5, allowPOS=('an', 'vn', 'n', 'nr', 'ns', 'nt', 'nz'))
    print("关键词:%s" % keywords)
    print("微博id:%s" % one_cluster.id_list)
    print("微博内容:%s" % one_cluster.title_list)
    print("起始时间:%s 结束时间:%s" % (one_cluster.first_title, one_cluster.last_title))
    print("总热度:%s" % one_cluster.hot)
    print("******************************")
    # f.write("cluster_index:%s\n" % index)
    # f.write("簇中结点个数为:%s\n" % one_cluster.node_num)
    # texts = "".join(one_cluster.title_list)  # 重新提取该簇的关键词
    # keywords = jieba.analyse.extract_tags(texts, topK=5, allowPOS=('an', 'vn', 'n', 'nr', 'ns', 'nt', 'nz'))
    # f.write("关键词:%s\n" % keywords)
    # f.write("微博id:%s\n" % one_cluster.id_list)
    # f.write("微博内容:%s\n" % one_cluster.title_list)
    # f.write("微博时间:%s\n" % one_cluster.time_list)
    # f.write("起始时间:%s 结束时间:%s\n" % (one_cluster.first_title, one_cluster.last_title))
    # f.write("总热度:%s\n\n" % one_cluster.hot)
    # f.write("******************************")
    for i in range(len(one_cluster.time_list)):
        one_cluster.time_list[i] = re.sub(r' .*$', "", one_cluster.time_list[i])
    values = one_cluster.time_list
    values_counts = Counter(values)
    a = values_counts.keys()
    b = values_counts.values()
    f = open('wordcloud.txt', "w+", encoding="utf8")
    for i in range(len(one_cluster.title_list)):
        f.write(one_cluster.title_list[i])
    f.close()


X = a
Y = b
fig = plt.figure(figsize=(10, 4))
plt.bar(X, Y, 0.4, color="green")
plt.xlabel("date")
plt.ylabel("weibo amount")
plt.title("weibo trend")

plt.show()
# plt.savefig("barChart.jpg")
