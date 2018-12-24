# -*- coding: utf-8 -*-
# @Time    : 2018/12/24 10:45
# @Author  : zcc
# @File    : remove_only_person.py
# @Function:

#coding=utf-8
import xml.etree.ElementTree as ET
import os
import shutil
def modify_xml(path):
    updateTree = ET.parse(path)
    root = updateTree.getroot()
    # 修改sub2的数据值
    label_text=[]
    for object in root.findall('object'):  # 找到root节点下的所有object节点
        if object.find('name').text !='person':
            label_text.append(object.find('name').text)
    # print(label_text)
    return len(label_text)
    # updateTree.write(path)

def mkr(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

if __name__ == '__main__':
    # xml_path='E:/datasets/VOCdevkit/VOC2012/Annotations_ssd/'
    # dst_xml_path='E:/datasets/VOCdevkit/VOC2012/Annotations_notperson/'
    # img_path='E:/datasets/VOCdevkit/VOC2012/JPEGImages_ssd/'
    # dst_img_path='E:/datasets/VOCdevkit/VOC2012/JPEGImages_notperson/'

    xml_path = 'E:/datasets/COCO/coco2017_result/Annotations/'
    dst_xml_path = 'E:/datasets/COCO/coco2017_result/Annotations_notperson/'
    img_path = 'E:/datasets/COCO/coco2017_result/images/'
    dst_img_path = 'E:/datasets/COCO/coco2017_result/JPEGImages_notperson/'
    mkr(dst_xml_path)
    mkr(dst_img_path)
    for i in os.listdir(xml_path):
       l= modify_xml(xml_path+i)
       img_name=i.split('.')[0]+'.jpg'
       if l:
           shutil.copy(xml_path+i, dst_xml_path+i)
           shutil.copy(img_path+img_name, dst_img_path+img_name)

