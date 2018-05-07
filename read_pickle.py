import pickle
import jieba.analyse
# 读取保存的簇
pkl_file = open('data.pkl', 'rb')
new_data = pickle.load(pkl_file)
pkl_file.close()
new_data.top = 10  # 修改显示的簇数量
# new_data.printClusterResult()

print_cluster_list = sorted(new_data.cluster_list, key=lambda ClusterUnit: ClusterUnit.node_num, reverse=True)[:new_data.top]
for index, one_cluster in enumerate(print_cluster_list):
    print("cluster_index:%s" % index)
    print("簇中结点个数为:%s" % one_cluster.node_num)
    texts = "".join(one_cluster.title_list)  # 重新提取该簇的关键词
    keywords = jieba.analyse.extract_tags(texts, topK=10)
    print("关键词:%s" % keywords)
    print("******************************")
