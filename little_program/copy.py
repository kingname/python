# -*- coding: utf8 -*-
#本文件将test下面所有文件夹中的jpg图片全部复制到pic文件夹下面
#This file is to copy the .jpg files into another dir. 
import os
import shutil
root=os.getcwd()
road=root+"\\test\\"
thedir = os.listdir(road)
for i in thedir:    
    path = road+ i
    picfile = os.listdir(path)
    for i in picfile:
    	print type(i)
        if i[-1]=='g':     
            
            res=path + "\\"+i
            des = root+"\\pic\\"+i
            shutil.copyfile (res, des)
print "finished!!"

