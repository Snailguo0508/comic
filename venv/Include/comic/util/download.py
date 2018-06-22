from urllib.request import urlopen
from urllib import request
from bs4 import BeautifulSoup
from urllib.error import HTTPError
import re
import pymysql
import JsonUtil
import os


urlList = []

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



def getPath(targetDir,path,num):
    if not os.path.exists(targetDir): #判断目录是否存在
        os.makedirs(targetDir) #创建多级目录
    pos = path.rindex('/')
    t = os.path.join(targetDir, '%s.jpg'%num)
    return t

def httpGet(url):
    try:
        urlopen(url)
    except HTTPError as h
        print("请求异常,url = " + url)
        return None
    else:
        html = BeautifulSoup(url,"lxml")


def downloadPic(name,picUrl):
    file = "E:\\"+ name + "\\" + title
    num = 1
    path = getPath(file, pic, num)
    request.urlretrieve(pic, path, Schedule)

def download(listSource):
    for source in listSource:
        title = JsonUtil.getHtmlResult(r'title=\"(.*?)\"', source)
        mainUrl = JsonUtil.getHtmlResult(r'href=\"(.*?)\"', source)
        mainUrl = localList[0] + mainUrl
        mainHtml = httpGet(mainUrl)
        if mainUrl is not None:
            picUrl = JsonUtil.getHtmlResult(r'mhurl=\"(.*?jpg)\"', mainHtml.decode())
            name = JsonUtil.getHtmlResult(r'CTitle=\"(.*?)\"', source)
            pic = "http://p1.xiaoshidi.net/" + picUrl
            if pic.index("2015") ==-1 or pic.index("2016")==-1 or pic.index("2017")==-1 or pic.index("2018")==-1:
                pic = pic.replace("p1","p0")
            downloadPic(name, picUrl)
        else:
            print("页面为空,url = " + mainUrl)




localList = getLocation();
for url in localList:
    listArray = getListHtml(url)
    if len(listArray):
        listSource = getListCode(listArray)
        if len(listSource):
            download(listSource)
    else:
        print(name + "列表页为空, url = " + url)












