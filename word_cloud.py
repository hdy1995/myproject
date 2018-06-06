# wordcloud生成中文词云

from wordcloud import WordCloud
import jieba
from scipy.misc import imread
from os import path
import matplotlib.pyplot as plt


# 绘制词云
def draw_wordcloud():
    # 读入一个txt文件
    comment_text = open('C:\\Users\Administrator\PycharmProjects\\untitled2\myproject\wordcloud1.txt', 'r',
                        encoding="utf8").read()
    # 结巴分词，生成字符串，如果不通过分词，无法直接生成正确的中文词云
    cut_text = " ".join(jieba.cut(comment_text))
    d = path.dirname(__file__)  # 当前文件文件夹所在目录
    color_mask = imread("D:\\baiduyundownload\Menhera酱表情包 无水印汉化版\Menhera酱表情包 无水印汉化版\\38.jpg")  # 读取背景图片
    cloud = WordCloud(
        # 设置字体，不指定就会出现乱码
        font_path="C:\Windows\winsxs\\amd64_microsoft-windows-f..type-microsoftyahei_31bf3856ad364e35_6.1.7600.16385_none_96c833d749ca5140\msyh.ttf",
        # font_path=path.join(d,'simsun.ttc'),
        # 设置背景色
        background_color='white',
        # 词云形状
        mask=color_mask,
        # 允许最大词汇
        max_words=2000,
        # 最大号字体
        max_font_size=60
    )
    word_cloud = cloud.generate(cut_text)  # 产生词云
    # word_cloud.to_file("pjl_cloud4.jpg")  # 保存图片
    #  显示词云图片
    plt.imshow(word_cloud)
    plt.axis('off')
    plt.show()


if __name__ == '__main__':
    draw_wordcloud()
