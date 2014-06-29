# -*- coding: utf8 -*-
##本文件可以删除空文件夹
#This file is to delect all the empty dir.
import os
k=os.getcwd()
s=k+"\\test\\"
m = os.listdir(s)
for i in m:    
    path = s+ i
    if os.listdir(path) == []:
        os.rmdir(path)
