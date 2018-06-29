from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError

#https://manhua.fzdm.com/2/908/index_14.html

try:
    obj = urlopen("http://manhua.fzdm.com/2/909/index_15.html");

except HTTPError as e:
    print(e.code)
    #html = BeautifulSoup(obj,"lxml")
    #print(html)
