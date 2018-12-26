# -*- coding: utf-8 -*-
# @Time    : 2018/12/25 13:50
# @Author  : zcc
# @File    : kitti2voc.py
# @Function:

import os
import cv2
import glob
import sys
import numpy as np

image_path = "E:/datasets/kitti/data_object_image_2/training/image_2/"
label_path='E:/datasets/kitti/data_object_label_2/training/label_2/'

def rename_imagefile(path):
    for filename in os.listdir(path):
        #os.path.splitext分离文件名与扩展名
        if os.path.splitext(filename)[1] == '.png':
            img = cv2.imread(path + filename)
            print(filename.replace(".png", ".jpg"))
            newfilename = filename.replace(".png", ".jpg")
            cv2.imwrite(path + newfilename, img)
            os.remove(path+filename)
# rename_imagefile(image_path)
from PIL import Image, ImageDraw,ImageFont


def show_box(path):
    txt_list = glob.glob(path+'/*.txt')
    for item in txt_list[0:1500]:
        print(item.split('\\'))
        img_path=image_path+item.split('\\')[-1].split('.')[0]+'.jpg'
        img = Image.open(img_path)

        draw = ImageDraw.Draw(img)

        with open(item) as tdf:
            labels=[]
            for each_line in tdf:
                labeldata = each_line.strip().split(' ')  # 去掉前后多余的字符并把其分开
                print(labeldata)
                label=labeldata[0]  #第一个字段，即类别
                labels.append(label)
                if label=='Misc':
                    xmin=int(float(labeldata[4]))
                    ymin=int(float(labeldata[5]))
                    xmax=int(float(labeldata[6]))
                    ymax=int(float(labeldata[7]))
                    draw.rectangle([xmin, ymin, xmax, ymax])
                    draw.text([xmin, ymin], label, "red")
            if 'Misc' in labels:
                img.show()



