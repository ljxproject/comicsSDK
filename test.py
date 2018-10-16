# import os
#
import os  #打开文件时需要
import time
import datetime
from PIL import Image
import re
#
# Start_path= r'E:\work\comic_pj\comic\static\998\my\1'
# new_path = r'E:\work\comic_pj\comic\static\999\my\1'
# iphone5_width=600
# iphone5_depth=800
# list=os.listdir(Start_path)
# count=0
# for pic in list:
#     path=Start_path+"/"+pic
#     print(path)
#     im=Image.open(path)
#     w,h=im.size
#     #print w,h
#     #iphone 5的分辨率为1136*640，如果图片分辨率超过这个值，进行图片的等比例压缩
#
#     if w>iphone5_width:
#         print( pic)
#         print ("图片名称为"+pic+"图片被修改")
#         h_new=int(iphone5_width*h/w)
#         w_new=int(iphone5_width)
#         count=count+1
#         out = im.resize((w_new,h_new),Image.ANTIALIAS)
#         out.save(new_path +"/"+pic)
#
#     if h>iphone5_depth:
#         print (pic)
#         print ("图片名称为"+pic+"图片被修改")
#         w_new=int(iphone5_depth*w/h)
#         h_new=int(iphone5_depth)
#         count=count+1
#         out = im.resize((w_new,h_new),Image.ANTIALIAS)
#         out.save(new_path+"/"+pic)
#
# print ('END')
# count=str(count)
# print ("共有"+count+"张图片尺寸被修改")
# s = "update api_imgresource set my_title='%s',chap_cover_img='%s',my_img_list_path='%s',price='%s' where %s" \
#     % ('chapter 14', '', '999/my/14', '0.19', "com_id='999' and chap_id='14'")
# print(s)
import operator
l = {2:"DDV",1:"Vds",3:"vnfv"}
a = sorted(l.items(),key=operator.itemgetter(0),reverse=False)
print(dict(a))