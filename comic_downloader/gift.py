# -*- coding: utf-8 -*-  

#本程序下载卖肉漫画
#使用请翻墙
#大部分功能完成
#做好以后，送个室友当生日礼物。

import urllib    
import urllib2
import re
import sys
import os
import wx
import threading
import random
root = os.getcwd()
verson = '1.25'
author = 'kingname'
reload(sys)
sys.setdefaultencoding('utf-8')
page = 2
url = 'http://50.117.115.70/thread-htm-fid-20-page-'
headers = {
	
	       #"GET":url,
	       "Host":"cncaomm.com",
	       "referer":"cncaomm.com",
	       "User-Agent":"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36" 
}

class WorkerThread(threading.Thread):
	def __init__(self,img_url,comic_path):
		threading.Thread.__init__(self)
		self.url = img_url
		self.count = 0
		self.comic_path = comic_path
		self.leave = threading.Event()
		self.leave.clear()		

	def stop(self):
		#self.leave.set()
		self.thread_stop = True 
		self.count = 0
		frame.multiText2.AppendText(u'下载终止\n')

	def run(self):
		img_add = re.findall('<img src="(.*?)" border="0"',self.url,re.S)
		num = 0
		#for i in img_add:
		self.count = len(img_add)
		while num< self.count:
			i = img_add[num]
			img_path = self.comic_path + '\\' + str(num) + '.' + i[-3:]
			down_img(i,img_path)
			wx.CallAfter(Setmessage,img_path)
			num +=1	
		frame.multiText2.AppendText(u'下载完成\n')	

class myFrame(wx.Frame): 
	def __init__(self):  
			wx.Frame.__init__(self, None, -1, u'卖肉漫画下载器v1.25',   
				size=(780, 730))  
			panel = wx.Panel(self, -1) 
			basicLabel = wx.StaticText(panel, -1, u"漫画列表:",) 
			basicLabel2 = wx.StaticText(panel, -1, u"下载状态：",(380,400)) 
			basicLabel3 = wx.StaticText(panel, -1, u"在线看漫画功能下个版本开发",(480,200))
			self.multiText2 = wx.TextCtrl(panel, -1,  
					u"下载状态\n",  
					size=(380, 200),pos= (380,420), style=wx.TE_MULTILINE+wx.TE_READONLY) #创建一个文本控件
			self.comic_name_list = [] 
			self.listBox = wx.ListBox(panel, -1, (5, 20), (350, 600), self.comic_name_list,   
							wx.LB_SINGLE)
			sizer = wx.FlexGridSizer(rows=3,cols=2, hgap=6, vgap=6)
			sizer.AddMany([basicLabel])  
			panel.SetSizer(sizer)
			self.button_Onload = wx.Button(panel, -1, u"加载首页", pos=(130, 630)) 
			self.button_Onnext = wx.Button(panel, -1, u"下一页>>", pos=(230, 630)) 
			self.button_Onjust = wx.Button(panel, -1, u"<<上一页", pos=(30, 630)) 
			self.button_Ondown = wx.Button(panel, -1, u"开始下载", pos=(380, 630)) 
			self.button_Oncancle = wx.Button(panel, -1, u"停止下载", pos=(470, 630))
			self.Bind(wx.EVT_BUTTON, self.Onload, self.button_Onload)
			self.Bind(wx.EVT_BUTTON, self.Onnext, self.button_Onnext)
			self.Bind(wx.EVT_BUTTON, self.Onjust, self.button_Onjust)
			self.Bind(wx.EVT_BUTTON, self.Ondown, self.button_Ondown)
			self.Bind(wx.EVT_BUTTON, self.Oncancle, self.button_Oncancle)
			self.Bind(wx.EVT_CLOSE,  self.OnCloseWindow)
			self.button_Onload.SetDefault()
			self.button_Onnext.SetDefault()
			self.button_Onjust.SetDefault()
			self.button_Ondown.SetDefault()
			self.button_Oncancle.SetDefault()
	
	#加载首页漫画列表		
	def Onload(self, event):
		addr = url + '2.html'
		self.comic_list = get_list(addr)


	#加载下一页漫画列表
	def Onnext(self,event):
		global page
		page += 1
		#frame.multiText.Clear() 
		addr = url + str(page) + '.html'
		self.comic_list = get_list(addr)
	
	#上一页漫画列表
	def Onjust(self,event):  
		global page
		if page >= 3:
			page -=1
			#frame.multiText.Clear()
			addr = url + str(page) + '.html'
			self.comic_list = get_list(addr)
	#下载漫画
	def Ondown(self,event):
		comic_number = self.listBox.GetSelections()
		#Setmessage(u'开始下载!\n')
		frame.multiText2.AppendText(u"开始下载！\n")
		down_start(self.comic_list,list(comic_number)[0])
	
	#取消下载
	def  Oncancle(self,event):
		thethread.stop()
		#Setmessage(u'下载取消！')
		frame.multiText2.AppendText(u'下载取消！\n')

	def OnCloseWindow(self, event):
		thethread.stop()
		self.Destroy()

#发送信息到GUI节目
def Setmessage(info):
		frame.multiText2.AppendText(info.decode('gbk','ignore')+"\n")


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

#下载图片漫画
def down_img(i,img_path):
	try:		
		data = urllib.urlretrieve(i,img_path)
	except Exception as e:
		frame.multiText2.AppendText(u'下载出错，跳过本张图片\n')
		#print "err"
		#Setmessage('下载出错，跳过本张图片！')

#获取漫画列表
def get_list(url):
	sourse = get_page_sourse(url)
	list_group = re.findall('orderThreadsClass.orderThreads(.*?)<form action="thread.php',sourse,re.S)
	page_address = re.findall('<a name=.*?></a><a href="(.*?)" id="a_ajax.*? class="subject">(.*?)</a>',list_group[0],re.S)
	number = 1

	for i in page_address:
		if i[1][0] == '<':
			name = i[1][23:-11]
		else:
			name = i[1]
		#chardet_detect_str_encoding(name)
		name = '[' + str(number) + ']' + name  
		number += 1
		#frame.multiText.AppendText(name.decode('gbk','ignore')+"\n")
		frame.listBox.Append(name.decode('gbk','ignore'))
	return page_address

# 为每个漫画新建文件夹,如果名字重复，则文件夹名后面加上随机数字
def to_make_dir(path):
	new_path = os.path.join(root, path)
	if os.path.isdir(new_path):
		new_path += str(random.randint(1,20))
	os.makedirs(new_path)


#开始下载的函数
def down_start(comic_list,comic_number):
	global thethread
	if comic_list[comic_number][0] =='<':
		name = comic_list[comic_number][23:-11]
	else:
		name = comic_list[comic_number][1]
	try:
		to_make_dir(name)
		comic_path = root + '\\' + name

	except Exception as e:
		dir_name = 'comic'+str(random.randint(10,20))
		to_make_dir(dir_name)	
		comic_path = root + '\\' + dir_name
	img_page_address = 'http://cncaomm.com/' + comic_list[comic_number][0]
	img_page_html = get_page_sourse(img_page_address)
	img_url = get_img_url(img_page_html)
	thread = WorkerThread(img_url[0],comic_path)
	thethread = thread
	thread.start()


if __name__ == '__main__':
    app = wx.App()  
    frame = myFrame()  
    frame.Show()  
    app.MainLoop()  


