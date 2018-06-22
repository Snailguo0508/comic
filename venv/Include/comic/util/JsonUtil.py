import json
import re
import os


#正则匹配单个结果
def getHtmlResult(regexs,htmlCode):
    try:
        source = re.search(regexs, htmlCode, re.M|re.I)
        return source.group(1)

    except Exception as e:
        print("正则匹配结果异常,正则表达式为：" + regexs)
        return None




