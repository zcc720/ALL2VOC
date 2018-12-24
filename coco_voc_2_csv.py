# -*- coding: utf-8 -*-
# @Time    : 2018/12/24 16:17
# @Author  : zcc
# @File    : coco_voc_2_csv.py
# @Function:针对两点修改：1.voc2012中出现了filename缺少.jpg的现象. 2.voc2009中出现没有图片长宽通道信息 针对这两点补全

import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
import cv2
# os.chdir('E:/code/Widerface/widerface/')
path = 'E:/datasets/Six_classes/'

def xml_to_csv(path):
    xml_list = []
    for xml_file in glob.glob(path + 'Annotations/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        img_path = 'E:/datasets/Six_classes/JPEGImages/' + xml_file.split('\\')[-1].split('.')[0]+'.jpg'
        print(img_path)
        img = cv2.imread(img_path)
        W = img.shape[1]
        H = img.shape[0]
        for member in root.findall('object'):
            if not root.find('filename').text.endswith('.jpg'):
                root.find('filename').text=root.find('filename').text+'.jpg'
            value = (root.find('filename').text,
                     W,
                     H,
                     member[0].text,
                     int(member[4][0].text),
                     int(member[4][1].text),
                     int(member[4][2].text),
                     int(member[4][3].text)
                     )
            xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df


def main():
    xml_path = path
    xml_df = xml_to_csv(xml_path)
    xml_df.to_csv('coco_voc_6.csv')
    print('Successfully converted xml to csv.')

main()