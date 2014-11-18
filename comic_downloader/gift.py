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
import time
root = os.getcwd()
verson = '1.40'
author = 'kingname'
reload(sys)
sys.setdefaultencoding('utf-8')
page = 2
down = 0
preview_down = 0
#url = 'http://50.117.115.70/thread-htm-fid-20-page-'
url = 'https://cncaomm.com/thread-htm-fid-20-page-'
headers = {
	
	       #"GET":url,
	       "Host":"cncaomm.com",
	       "referer":"cncaomm.com",
	       "User-Agent":"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36" 
}

class WorkerThread(threading.Thread):
	def __init__(self,img_url,comic_path,preview = 0):
		threading.Thread.__init__(self)
		self.url = img_url
		self.count = 0
		self.preview = preview
		self.comic_path = comic_path
		self.leave = threading.Event()
		self.leave.clear()		

	def stop(self):
		#self.leave.set()
		self.thread_stop = True 
		self.count = 0
		frame.multiText2.AppendText(u'下载终止\n')

	def run(self):
		global preview_down
		img_add = re.findall('<img src="(.*?)" border="0"',self.url,re.S)
		num = 0
		#for i in img_add:
		if self.preview == 1:
			self.count = 1
		else:
			self.count = len(img_add)
		while num< self.count:
			i = img_add[num]
			img_path = self.comic_path + '\\' + str(num) + '.' + i[-3:]
			down_img(i,img_path)
			wx.CallAfter(Setmessage,img_path)
			num +=1	
		preview_down = 1
		frame.multiText2.AppendText(u'下载完成\n')	

class myFrame(wx.Frame): 
	def __init__(self):  
			wx.Frame.__init__(self, None, -1, u'卖肉漫画下载器v1.40  by 青南',   
				size=(780, 730))  
			panel = wx.Panel(self, -1) 
			basicLabel = wx.StaticText(panel, -1, u"漫画列表:",) 
			basicLabel2 = wx.StaticText(panel, -1, u"下载状态：",(380,420)) 
			basicLabel3 = wx.StaticText(panel, -1, u"漫画首页预览",(480,200))
			self.multiText2 = wx.TextCtrl(panel, -1,  
					u"下载状态\n",  
					size=(380, 180),pos= (380,440), style=wx.TE_MULTILINE+wx.TE_READONLY) #创建一个文本控件
			self.comic_name_list = [] 
			self.listBox = wx.ListBox(panel, -1, (5, 20), (350, 600), self.comic_name_list,   
							wx.LB_SINGLE)
			sizer = wx.FlexGridSizer(rows=3,cols=2, hgap=6, vgap=6)
			sizer.AddMany([basicLabel])
			panel.SetSizerAndFit(sizer)
			self.button_Onload = wx.Button(panel, -1, u"加载首页", pos=(130, 630)) 
			self.button_Onnext = wx.Button(panel, -1, u"下一页>>", pos=(230, 630)) 
			self.button_Onjust = wx.Button(panel, -1, u"<<上一页", pos=(30, 630)) 
			self.button_Ondown = wx.Button(panel, -1, u"开始下载", pos=(470, 630)) 
			self.button_Oncancle = wx.Button(panel, -1, u"停止下载", pos=(560, 630))
			self.button_Onpreview = wx.Button(panel, -1, u"预览首页", pos=(380, 630))
			self.Bind(wx.EVT_BUTTON, self.Onload, self.button_Onload)
			self.Bind(wx.EVT_BUTTON, self.Onnext, self.button_Onnext)
			self.Bind(wx.EVT_BUTTON, self.Onjust, self.button_Onjust)
			self.Bind(wx.EVT_BUTTON, self.Ondown, self.button_Ondown)
			self.Bind(wx.EVT_BUTTON, self.Oncancle, self.button_Oncancle)
			self.Bind(wx.EVT_BUTTON, self.Onpreview, self.button_Onpreview)
			self.Bind(wx.EVT_CLOSE,  self.OnCloseWindow)
			self.button_Onload.SetDefault()
			self.button_Onnext.SetDefault()
			self.button_Onjust.SetDefault()
			self.button_Ondown.SetDefault()
			self.button_Oncancle.SetDefault()
			self.button_Onpreview.SetDefault()
	
	#加载首页漫画列表		
	def Onload(self, event):
		addr = url + '2.html'
		self.listBox.Clear()
		self.comic_list = get_list(addr)


	#加载下一页漫画列表
	def Onnext(self,event):
		global page
		page += 1
		#frame.multiText.Clear() 
		addr = url + str(page) + '.html'
		self.listBox.Clear()
		self.comic_list = get_list(addr)
	
	#上一页漫画列表
	def Onjust(self,event):  
		global page
		if page >= 3:
			page -=1
			#frame.multiText.Clear()
			addr = url + str(page) + '.html'
			self.listBox.Clear()
			self.comic_list = get_list(addr)

	#预览漫画首页
	def Onpreview(self,event):
		global preview_down 
		preview_down = 0
		flag = 0
		n = 0
		comic_number = self.listBox.GetSelections()
		if comic_number == ():
			frame.multiText2.AppendText(u"请先选择一本漫画！\n")
		else:
			down_start(self.comic_list,list(comic_number)[0],preview = 1)
			while preview_down ==0:
				time.sleep(0.5)
				n +=1
				if n > 10:
					frame.multiText2.AppendText(u"预览出错了。。换一本漫画吧。。。\n")
					flag = 1	
					break 
			if flag == 0:
				try:
					img2 = wx.Image('.\\preview\\0.jpg',wx.BITMAP_TYPE_ANY)
					img1 = img2.Scale(370,400)
					sb1 = wx.StaticBitmap(self, -1, wx.BitmapFromImage(img1),pos = (380,20))
				except Exception as e:
					frame.multiText2.AppendText(u"预览出错了。。换一本漫画吧。。。\n")

	#下载漫画
	def Ondown(self,event):
		global down
		comic_number = self.listBox.GetSelections()
		if comic_number == ():
			frame.multiText2.AppendText(u"请先选择一本漫画！\n")
		else:			
		#Setmessage(u'开始下载!\n')
			frame.multiText2.AppendText(u"开始下载！\n")
			down = 1
			down_start(self.comic_list,list(comic_number)[0])
		
	#取消下载
	def  Oncancle(self,event):
		global down
		if down == 1:
			thethread.stop()
			#Setmessage(u'下载取消！')
			frame.multiText2.AppendText(u'下载取消！\n')
		else:
			frame.multiText2.AppendText(u'还未下载，谈何取消？\n')

	def OnCloseWindow(self, event):
		global down
		if down == 1:
			thethread.stop()
			down = 0
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
def to_make_dir(path,preview = 0):
	new_path = os.path.join(root, path)
	if not os.path.isdir(new_path):
		os.makedirs(new_path)
	else:
		if preview == 0:
			if os.path.isdir(new_path):
				new_path += str(random.randint(1,100))
			os.makedirs(new_path)

#开始下载的函数
def down_start(comic_list,comic_number,preview = 0):
	global thethread
	if preview == 1:
		name = 'preview'
		to_make_dir(name,preview = 1)
		comic_path = root + '\\' + name
	else:
		if comic_list[comic_number][0] =='<':
			name = comic_list[comic_number][23:-11]
		else:
			name = comic_list[comic_number][1]
		try:
			to_make_dir(name)
			comic_path = root + '\\' + name

		except Exception as e:
			dir_name = 'comic'+str(random.randint(10,100))
			to_make_dir(dir_name)	
			comic_path = root + '\\' + dir_name
	#img_page_address = 'http://cncaomm.com/' + comic_list[comic_number][0]
	img_page_address = 'https://cncaomm.com/' + comic_list[comic_number][0]
	img_page_address = re.sub('-fpage-\d+','',img_page_address)
	img_page_html = get_page_sourse(img_page_address)
	img_url = get_img_url(img_page_html)
	thread = WorkerThread(img_url[0],comic_path,preview)
	thethread = thread
	thread.start()


if __name__ == '__main__':
    app = wx.App()  
    frame = myFrame()  
    frame.Show()  
    app.MainLoop()  


