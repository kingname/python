# -*- coding: utf-8 -*-  
import urllib    
import urllib2
import string
import wx 
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')   
road = r'E:\\github\\kingname.github.io\\'
website = 'http://www.jwc.uestc.edu.cn/news/queryList.do?parameters[%27part_id%27]=37'
site = 'http://www.jwc.uestc.edu.cn/'
headers = {
	
	       #"GET":url,
	       "Host":"www.jwc.uestc.edu.cn",
	       "referer":"http://www.jwc.uestc.edu.cn/",
	       "User-Agent":"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36" 
}

def getsourse(url):
	req = urllib2.Request(url)
	for key in headers:
		req.add_header(key,headers[key])
	return urllib2.urlopen(req).read().decode("utf-8")
def spider_context(url,title):
	file_name =road + title + ".html"         
	code = getsourse(url)
	#code = html.decode("utf-8") 
	info = re.findall(u'<!--用户导航结束-->(.*?)<!--文章内容-->',code,re.S)
	info2 = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
</head>''' + info[0]
	output = open(file_name,'w')
	output.write(info2)
	output.close()
#title = (u"教学管理2")
#spider_context(title)
def spider_title():
	sourse = getsourse(website)
	info = re.findall(u'<!--新闻列表显示-->.*?<!--新闻列表显示结束-->',sourse,re.S)
	subinfo = re.findall('href="(.*?)" title="(.*?)">',info[0],re.S)
	news = []
	for new in subinfo:
		url = site + new[0]
		print url
		print new[1]
		spider_context(url,new[1])

spider_title()
