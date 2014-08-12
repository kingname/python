# -*- coding: utf-8 -*-  

#本程序下载卖肉漫画
#使用请翻墙
#已经实现基本功能
#已知bug: 下载漫画时，图形界面会卡死，但是仍然在继续下载。正在尝试解决。

import urllib    
import urllib2
import re
import sys
import os
import wx
import chardet;
root = os.getcwd()
verson = '1.00'
author = 'kingname'
down = 0
reload(sys)
sys.setdefaultencoding('utf-8')
#website = 'http://cncaomm.com/read-htm-tid-4246106.html'
page = 2
url = 'http://cncaomm.com/thread-htm-fid-20-page-'
headers = {
	
	       #"GET":url,
	       "Host":"cncaomm.com",
	       "referer":"cncaomm.com",
	       "User-Agent":"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36" 
}


class myFrame(wx.Frame): 
	def __init__(self):  
			wx.Frame.__init__(self, None, -1, u'卖肉漫画下载器v1.00',   
				size=(780, 730))  
			panel = wx.Panel(self, -1) 
			basicLabel = wx.StaticText(panel, -1, u"漫画列表:",) 
			basicLabel2 = wx.StaticText(panel, -1, u"下载状态：",(380,400)) 
			basicLabel3 = wx.StaticText(panel, -1, u"在线看漫画功能下个版本开发",(480,200))
			basicLabel4 = wx.StaticText(panel, -1, u"输入漫画序号:",(380,630))
			self.basicText = wx.TextCtrl(panel, -1, "",  size=(100, -1),pos = (470,625))  
			self.basicText.SetInsertionPoint(0)
			self.multiText = wx.TextCtrl(panel, -1,  
					u"",  
					size=(350, 600),pos= (5,20), style=wx.TE_MULTILINE+wx.TE_READONLY) #创建一个文本控件
			self.multiText2 = wx.TextCtrl(panel, -1,  
					u"下载状态",  
					size=(380, 200),pos= (380,420), style=wx.TE_MULTILINE+wx.TE_READONLY) #创建一个文本控件
			sizer = wx.FlexGridSizer(rows=3,cols=2, hgap=6, vgap=6)
			sizer.AddMany([basicLabel])  
			panel.SetSizer(sizer)
			self.button_Onload = wx.Button(panel, -1, u"加载首页", pos=(130, 630)) 
			self.button_Onnext = wx.Button(panel, -1, u"下一页>>", pos=(230, 630)) 
			self.button_Onjust = wx.Button(panel, -1, u"<<上一页", pos=(30, 630)) 
			self.button_Ondown = wx.Button(panel, -1, u"开始下载", pos=(580, 630)) 
			self.button_Oncancle = wx.Button(panel, -1, u"停止下载", pos=(670, 630))
			self.Bind(wx.EVT_BUTTON, self.Onload, self.button_Onload)
			self.Bind(wx.EVT_BUTTON, self.Onnext, self.button_Onnext)
			self.Bind(wx.EVT_BUTTON, self.Onjust, self.button_Onjust)
			self.Bind(wx.EVT_BUTTON, self.Ondown, self.button_Ondown)
			self.Bind(wx.EVT_BUTTON, self.Oncancle, self.button_Oncancle)
			self.button_Onload.SetDefault()
			self.button_Onnext.SetDefault()
			self.button_Onjust.SetDefault()
			self.button_Ondown.SetDefault()
			self.button_Oncancle.SetDefault()
			
	def Onload(self, event):
		#down_start(url)
		addr = url + '2.html'
		self.comic_list = get_list(addr)
		#frame.multiText.AppendText(u"开始下载！\n")
	def Onnext(self,event):
		global page
		page += 1
		frame.multiText.Clear() 
		addr = url + str(page) + '.html'
		self.comic_list = get_list(addr)
	def Onjust(self,event):
		global page
		if page >= 3:
			page -=1
			frame.multiText.Clear()
			addr = url + str(page) + '.html'
			self.comic_list = get_list(addr)
	def Ondown(self,event):
		global down
		down  = 1
		comic_number = int(self.basicText.GetValue()) - 1
		down_start(self.comic_list,comic_number)
	def  Oncancle(self,event):
		global down
		down = 0


#获取页面源代码
def get_page_sourse(url):
	req = urllib2.Request(url)
	for key in headers:
		req.add_header(key,headers[key])
	return urllib2.urlopen(req).read().decode('utf-8', 'ignore').encode('gb2312','ignore')
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
		if down == 1:
			path2 = comic_path + '\\' + str(num) + '.' + 'jpg'
			try:		
				data = urllib.urlretrieve(i,path2)
				frame.multiText2.AppendText(path2.decode('gbk','ignore')+"\n")
				num += 1
			except Exception as e:
				frame.multiText2.AppendText(u'下载出错，跳过本张图片\n')
		else:
			frame.multiText2.AppendText(u'下载取消！\n')
	frame.multiText2.AppendText(u'下载完成\n')

#获取漫画列表
def get_list(url):
	sourse = get_page_sourse(url)
	list_group = re.findall('orderThreadsClass.orderThreads(.*?)<form action="thread.php',sourse,re.S)
	page_address = re.findall('<a name=.*?></a><a href="(.*?)" id="a_ajax.*? class="subject">(.*?)</a>',list_group[0],re.S)
	number = 1
	#for i in page_address:
	#	s = 'cncaomm.com/' + i[0]
	for i in page_address:
		if i[1][0] == '<':
			name = i[1][23:-11]
		else:
			name = i[1]
		#chardet_detect_str_encoding(name)
		name = '[' + str(number) + ']' + name  
		number += 1
		frame.multiText.AppendText(name.decode('gbk','ignore')+"\n")
	return page_address

# 为每个漫画新建文件夹
def to_make_dir(path):
	new_path = os.path.join(root, path)
	if os.path.isdir(new_path):
		new_path += '_new'
	os.makedirs(new_path)

#开始下载
def down_start_consloe(url):
	n = 0
	page_address = get_list(url)
	for i in page_address:
		if i[1][0] == '<':
			name = i[1][23:-11]
		else:
			name = i[1]
		frame.multiText.AppendText(name+"\n")
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

def down_start(comic_list,comic_number):
	n = 0
	if comic_list[comic_number] =='<':
		name = comic_list[comic][23:-11]
	else:
		name = comic_list[comic_number][1]
	try:
		to_make_dir(name)
		comic_path = root + '\\' + name
	except Exception as e:
		to_make_dir('comic'+str(n))	
		comic_path = root + '\comic' + str(n)
		n += 1
	img_page_address = 'http://cncaomm.com/' + comic_list[comic_number][0]
	img_page_html = get_page_sourse(img_page_address)
	img_url = get_img_url(img_page_html)
	down_img(img_url[0],comic_path)

#down_start(url)

if __name__ == '__main__':
    app = wx.App()  
    frame = myFrame()  
    frame.Show()  
    app.MainLoop()  


