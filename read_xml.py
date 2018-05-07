#!/usr/bin/python3

import xml.sax
import re


class WeiboHandler(xml.sax.ContentHandler):

    def __init__(self):
        self.CurrentData = ""
        self.id = ""
        self.Id = []
        self.article = ""
        self.Article = []
        self.time = ""
        self.Time = []

    # 元素开始调用
    def startElement(self, tag, attributes):
        self.CurrentData = tag

    # 元素结束调用
    # 标签名根据xml文件自身情况更改
    def endElement(self, tag):
        # if self.CurrentData == "id":
        if self.CurrentData == "weiboId":
            # print("id:", self.id)
            self.Id.append(self.id)
            # print("Id:", self.Id)
        # elif self.CurrentData == "article":
        elif self.CurrentData == "text":
            self.article = re.sub(r'【.*?要闻回顾】|转发微博|\[.*?\]|（分享自 @.*?）|（来自.*?）|（via.*?）|奉上今日《台州商报》主要内容|@ .*? |@.*? |//@.*$|→[a-zA-z]+://[^\s]*|[a-zA-z]+://[^\s]*| - .*$|_.*? |&.*?;|quot;|apos;|amp;|lt;|gt;', "", self.article)
            # print("article:", self.article)
            # self.article = re.findall(r'#.*?#', self.article)
            # print("重点:", self.article)
            self.Article.append(self.article)
            # print("Article:", Article)
        # elif self.CurrentData == "time":
        elif self.CurrentData == "created_at":
            # print("time:", self.time)
            self.Time.append(self.time)
        self.CurrentData = ""

    # 读取字符时调用
    def characters(self, content):
        # if self.CurrentData == "id":
        if self.CurrentData == "weiboId":
            self.id = content
        # elif self.CurrentData == "article":
        elif self.CurrentData == "text":
            self.article = content
        # elif self.CurrentData == "time":
        elif self.CurrentData == "created_at":
            self.time = content


def read_xml(file):
    # 创建一个 XMLReader
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    # 重写 ContextHandler
    Handler = WeiboHandler()
    parser.setContentHandler(Handler)
    # parser.parse('test.xml')
    parser.parse(file)
    return Handler.Id, Handler.Article, Handler.Time
