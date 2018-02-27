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
        self.discuss = ""
        self.Discuss = []
        self.insertTime = ""
        self.InsertTime= []
        self.transmit = ""
        self.Transmit = []

    # 元素开始调用
    def startElement(self, tag, attributes):
        self.CurrentData = tag
        # if tag == "RECORD":
            # print("*****RECORD*****")
            # title = attributes["title"]
            # print("Title:", title)

    # 元素结束调用
    def endElement(self, tag):
        if self.CurrentData == "id":
            # print("id:", self.id)
            self.Id.append(self.id)
            # print("Id:", Id)
        elif self.CurrentData == "article":
            self.article = re.sub(r'@ .*? |@.*? |//@.*$|[a-zA-z]+://[^\s]*|[→]|转发微博|分享图片|手机测试|_.*? ', "", self.article)

            # print("article:", self.article)
            # self.article = re.findall(r'#.*?#', self.article)
            # print("重点:", self.article)

            self.Article.append(self.article)
            # print("Article:", Article)
        elif self.CurrentData == "discuss":
            # print("discuss:", self.discuss)
            self.Discuss.append(self.discuss)
        elif self.CurrentData == "insertTime":
            # print("insertTime:", self.insertTime)
            self.InsertTime.append(self.insertTime)
        elif self.CurrentData == "transmit":
            # print("transmit:", self.transmit)
            self.Transmit.append(self.transmit)
        self.CurrentData = ""

    # 读取字符时调用
    def characters(self, content):
        if self.CurrentData == "id":
            self.id = content
        elif self.CurrentData == "article":
            self.article = content
        elif self.CurrentData == "discuss":
            self.discuss = content
        elif self.CurrentData == "insertTime":
            self.insertTime = content
        elif self.CurrentData == "transmit":
            self.transmit = content

def read_xml():
#if __name__ == "__main__":
    # 创建一个 XMLReader
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    # 重写 ContextHandler
    Handler = WeiboHandler()
    parser.setContentHandler(Handler)
    parser.parse("test.xml")
    return Handler.Id, Handler.Article, Handler.Discuss, Handler.InsertTime, Handler.Transmit

