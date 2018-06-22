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
            location = result[0]
            urlList.append(location.replace("https","http"))
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


localList = getLocation();

listArray = getListHtml(localList[41])

listSource = getListCode(listArray)
for source in  listSource:
    title = JsonUtil.getHtmlResult(r'title=\"(.*?)\"', source)
    mainUrl = JsonUtil.getHtmlResult(r'href=\"(.*?)\"', source)
    mainUrl = localList[0] + mainUrl
    mainObj = urlopen(mainUrl)
    mainHtml = BeautifulSoup(mainObj, "lxml")
    picUrl = JsonUtil.getHtmlResult(r'mhurl=\"(.*?jpg)\"', mainHtml.decode())
    size = JsonUtil.getHtmlResult(r'mhurl=\"(.*?jpg)\"', mainHtml.decode())
    pic = "http://p1.xiaoshidi.net/" + picUrl







file = "E:\海贼王"  + "\\"+ title
num = 1
path = getPath(file,pic,num)

request.urlretrieve(pic,path,Schedule)


