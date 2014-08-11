# -*- coding: utf-8 -*-  

#本程序下载卖肉漫画
#使用请翻墙
#功能尚不完善
#做好图形界面以后，送个室友当生日礼物。

import urllib    
import urllib2
import re
import sys
import os
root = os.getcwd()
verson = '1.00'
author = 'kingname'

reload(sys)
sys.setdefaultencoding('utf-8')
#website = 'http://cncaomm.com/read-htm-tid-4246106.html'
url = 'http://cncaomm.com/thread-htm-fid-20-page-2.html'
headers = {
	
	       #"GET":url,
	       "Host":"cncaomm.com",
	       "referer":"cncaomm.com",
	       "User-Agent":"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36" 
}
#获取页面源代码
def get_page_sourse(url):
	req = urllib2.Request(url)
	for key in headers:
		req.add_header(key,headers[key])
	return urllib2.urlopen(req).read().decode('utf-8', 'ignore').encode('gbk','ignore')
#通过正则表达式获得含有图片的代码块
def get_img_url(html):
	img_group = re.findall('<div class="f14" id="read_tpc">(.*?)<tr class="r_one" id="att_info_display">',html,re.S)
	return img_group
#图像文件后缀名
def name(address):
	if address.find('.jpg'):
		return 'jpg'
	else:
		return 'png'

#下载图片漫画
def down_img(img_group,comic_path):
	img_add = re.findall('<img src="(.*?)" border="0"',img_group,re.S)
	num = 0
	for i in img_add:
		path2 = comic_path + '\\' + str(num) + '.' + 'jpg'
		print path2
		try:		
			data = urllib.urlretrieve(i,path2)
			num += 1
		except Exception as e:
			print u'下载出错，跳过本图片！'

#获取漫画列表
def get_list(url):
	sourse = get_page_sourse(url)
	list_group = re.findall('orderThreadsClass.orderThreads(.*?)<form action="thread.php',sourse,re.S)
	page_address = re.findall('<a name=.*?></a><a href="(.*?)" id="a_ajax.*? class="subject">(.*?)</a>',list_group[0],re.S)
	for i in page_address:
		print 'cncaomm.com/' + i[0]
	return page_address

# 为每个漫画新建文件夹
def to_make_dir(path):
	new_path = os.path.join(root, path)
	if not os.path.isdir(new_path):
		os.makedirs(new_path)

#开始下载
def down_start(url):
	n = 0
	page_address = get_list(url)
	for i in page_address:
		if i[1][0] == '<':
			name = i[1][23:-11]
		else:
			name = i[1]
		try:
			to_make_dir(name)
			comic_path = root + '\\' + name
		except Exception as e:
			to_make_dir('comic'+str(n))			
			comic_path = root + '\comic' + str(n)
			n += 1
		img_page_address = 'http://cncaomm.com/' + i[0]
		print img_page_address
		img_page_html = get_page_sourse(img_page_address)
		img_url = get_img_url(img_page_html)
		down_img(img_url[0],comic_path)

down_start(url)


