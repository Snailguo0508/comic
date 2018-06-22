#coding=utf-8
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError
import re
import pymysql

#获取风之漫画所有漫画的列表地址
def getListHtml(url):
    try:
        result = urlopen(url)
    except HTTPError as e:
        print("访问的地址出现HttpError")
        return None
    try:
        html = BeautifulSoup(result, "lxml")
        list = html.find_all("div", {"class":"round"})
    except AttributeError as e:
        print("获取URL源码异常")
        return None
    return list;


#进一步获取列表页集合
def getListCode(webCode):
    listArray = []
    try:
        for i in range(len(webCode)):
            listSrc = webCode[i].decode()
            source = re.search(r"<li>(.*?)</li>",listSrc,re.M|re.I)
            listArray.append(source.group())
    except Exception as e:
        print("正则匹配出现异常")
        return None
    else:
        return listArray


#正则匹配单个结果
def getHtmlResult(regexs,htmlCode):
    try:
        source = re.search(regexs, htmlCode, re.M|re.I)
        return source.group(1)

    except Exception as e:
        print("正则匹配结果异常,正则表达式为：" + regexs)
        return None


def getConnect():
    try:
        connect = pymysql.connect("localHost", "root", "123", "python",use_unicode=True, charset="utf8")

        print("获取数据库连接成功")
        return connect;
    except Exception as e:
        print("获取数据库连接异常")
        return None


def save(sql):
    try:
        conn = getConnect()
        cursor = conn.cursor()
        cursor.execute(sql)
        print("数据插入成功")
        cursor.close()
        conn.commit()
    except Exception as e:
        print("保存数据异常")
        print(e)
        conn.rollback()
    conn.close()



hostUrl = "https://manhua.fzdm.com";
listCodes = getListHtml("http://manhua.fzdm.com")

if listCodes is None:
    print("请求异常")
elif not listCodes:
    print("列表为空")
else:
    listSource = getListCode(listCodes)
    for i in range(len(listSource)):
        listCode = listSource[i]
        title = getHtmlResult(r"title=\"(.*?)\"", listCode).replace("漫画", "")
        location = getHtmlResult(r"href=\"(.*?)\"", listCode)
        location = hostUrl + "/" + location
        imgUrl = getHtmlResult(r"src=\"(.*?)\"",listCode)
        imgUrl = "http:" + imgUrl;
        sql = "INSERT INTO comiclist (name,imgurl,location) VALUES('" + title + "','" + imgUrl + "','" + location + "')"
        save(sql)

    print("完成")
