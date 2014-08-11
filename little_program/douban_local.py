# -*- coding: utf-8 -*-  
#挖掘豆瓣中的成都妹子
import urllib    
import urllib2
import string
import re
import sys
import cookielib 
reload(sys)
sys.setdefaultencoding('utf-8')
cookie = cookielib.CookieJar()  
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie)) 
url = 'http://www.douban.com/people/malimalihoom/contacts'
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
	print code
	info = re.findall('<div class="clear"></div>(.*?)<div class="aside">',code,re.S)
	webaddress = re.findall('<dd><a href="(.*?)">(.*?)</a></dd></dl>')
	for i in webaddress:
		print webaddress[1]+"   webaddress:"+webaddress[0]
#spider_context(url)
response = opener.open('www.douban.com/people/F2Player/contacts')  
for item in cookie:
	print item