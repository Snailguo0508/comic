from urllib.request import urlopen
from urllib import request
from bs4 import BeautifulSoup
from urllib.error import HTTPError
import re
import pymysql
import JsonUtil
import os


urlList = []

#从数据库获取漫画的网页地址
def getLocation():
    try:
        connect = pymysql.connect("localhost", "root", "123", "python", use_unicode=True, charset="utf8")
        cursor = connect.cursor()
        sql = "SELECT location FROM comiclist"
        cursor.execute(sql)
        results = cursor.fetchall()
    except Exception as e:
        print(e)
    if results is not None:
        for result in  results:
            location = result[0].replace("https","http")

            urlList.append(location)
    return urlList

#获取网页源码 并获取漫画列表固定区域源码
def getListHtml(url):
    try:
        result = urlopen(url)
    except HTTPError as e:
        print("访问的地址出现HttpError")
        return None
    try:
        html = BeautifulSoup(result, "lxml")
        list = html.find_all("li", {"class":"pure-u-1-2 pure-u-lg-1-4"})
    except AttributeError as e:
        print("获取URL源码异常")
        return None
    return list;

#解析HTML源码  通过正则匹配出相应结果
def getListCode(webCode):
    listArray = []
    try:
        for i in range(len(webCode)):
            listSrc = webCode[i].decode()
            source = re.search(r"<li.*?>(.*?)</li>",listSrc,re.M|re.I)
            listArray.append(source.group(1))
    except Exception as e:
        print("正则匹配出现异常")
        return None
    else:
        return listArray


def Schedule(a, b, c):
    '''
    a:已经下载的数据块
    b:数据库块的大小
    c:远程文件的大小
    '''
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
        print('完成！')
    print('%.2f%%' % per)


# 创建图片下载的路径


#请求漫画正文  获取源码
def httpGet(url):
    try:
        htmlObj = urlopen(url)
    except HTTPError as h:
        print("请求异常,url = " + url + ",状态码：e.code")
        return None
    else:
        html = BeautifulSoup(htmlObj,"lxml")
        return html

#下载漫画到指定路径
def downloadPic(name,title,pic,num):
    file = "E:\\"+ name + "\\" + title
    if not os.path.exists(file): #判断目录是否存在
        os.makedirs(file) #创建多级目录
    path = os.path.join(file, '%s.jpg'%num)
    request.urlretrieve(pic, path, Schedule)


def download(listSource):
    for source in listSource:
        title = JsonUtil.getHtmlResult(r'title=\"(.*?)\"', source)
        mainUrl = JsonUtil.getHtmlResult(r'href=\"(.*?)\"', source)
        mainUrl = localList[0] + mainUrl
        downloadComic = True
        num = 0;
        while downloadComic:
            if mainUrl.find("index") == -1:
                mainUrl = mainUrl + "index_" + str(num) + ".html"
            else:
                mainUrl = mainUrl.split("index")[0] + "index_" + str(num) + ".html"
            mainHtml = httpGet(mainUrl)

            if mainHtml is not None:
                picUrl = JsonUtil.getHtmlResult(r'mhurl=\"(.*?jpg)\"', mainHtml.decode())
                name = JsonUtil.getHtmlResult(r'CTitle=\"(.*?)\"', mainHtml.decode())
                if picUrl.find("http") == -1:
                    picUrl = "http://p1.xiaoshidi.net/" + picUrl
                pic = picUrl
                if pic.find("2015") == -1 or pic.find("2016") == -1 or pic.find("2017") == -1 or pic.find("2018") == -1:
                    pic = pic.replace("p1", "p0")
                downloadPic(name, title, pic,(num+1))
                downloadComic = True
                num += 1
            else:
                print("页面为空,url = " + mainUrl)
                downloadComic = False




localList = getLocation();
listArray = getListHtml(localList[0])
if len(listArray):
    listSource = getListCode(listArray)
    if len(listSource):
        download(listSource)
    else:
        print(name + "列表页为空, url = " + url)












