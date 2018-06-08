from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError
import re


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
        source = re.search(regexs, htmlCode, re.M | re.I)
        return source.group(1)
    except Exception as e:
        print("正则匹配结果异常,正则表达式为：" + regexs)
        return None





listCode = getListHtml("https://manhua.fzdm.com")
if listCode is None:
    print("请求异常")
else:
    listSource = getListCode(listCode)

for i in range(len(listSource)):
    comic = listSource[i]
    title = getHtmlResult(r"title=\"(.*?)\"",comic).replace("漫画","")

    



