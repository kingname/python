# -*- coding: utf-8 -*-  
#本程序挖掘豆瓣TOP250里面的电影，并对其按评分进行排序
import urllib    
import urllib2
import string
import wx 
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
url = 'http://movie.douban.com/top250'
road = 'E:\\mystuff\\ss\\'
pages = [25,50,75,100,125,150,175,200,225]
all_movie = []

headers = {
	
	       "DNT":"1",
	       "Host":"movie.douban.com",
	       "User-Agent":"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36"
}

def getsourse(url):
	req = urllib2.Request(url)
	for key in headers:
		req.add_header(key,headers[key])
	return urllib2.urlopen(req).read().decode('utf-8','ignore').encode("gbk", 'ignore')
def spider_context(url):
	i = 0       
	code = getsourse(url)
	info = re.findall('<ol class="grid_view">(.*?)</ol>',code,re.S)
	mov_add = re.findall('</em>.*?<a href="(.*?)">',info[0],re.S)
	movie = re.findall('<img alt="(.*?)" src',info[0],re.S)
	star = re.findall('><em>(.*?)</em></span>',info[0],re.S)	
	for mov in movie:
		all_movie.append((mov,star[i],mov_add[i]))
		i = i + 1
	   #title = mov + "score:" + star[i] + '\n\n'	   			
	   #output.write(title)
	#output.close()
spider_context(url)
for page in pages: 
    address = 'http://movie.douban.com/top250?start=' + str(page) + '&filter=&type='
    spider_context(address)
thelist = sorted(all_movie, key=lambda student: student[1],reverse=True)
file_name =road + "top250_2.txt" 
output = open(file_name,'a')
for x in range(len(all_movie)):
	name0 = thelist[x]
	name = list(name0)
	title = str(name[0]) + "  score:" + str(name[1])+ " site: " + name[2] +'\n\n'	   			
	output.write(title)
output.close()