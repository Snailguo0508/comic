from urllib.request import urlopen
from bs4 import BeautifulSoup


html = urlopen("http://www.jojoft.com/main");

htmlObject = BeautifulSoup(html,"lxml");

print(htmlObject.findAll("div","class:indexlistitem"))