from urllib.request import urlopen
from bs4 import BeautifulSoup


#https://manhua.fzdm.com/2/908/index_14.html


obj = urlopen("http://manhua.fzdm.com/2/908/index_15.html");

html = BeautifulSoup(obj,"lxml")

print(html)