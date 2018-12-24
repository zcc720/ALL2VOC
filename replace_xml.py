# -*- coding: utf-8 -*-
# @Time    : 2018/12/21 15:41
# @Author  : zcc
# @File    : replace_xml.py
# @Function:voc2012中的摩托车类标签为motorbike,但是coco里面是motorcycle,我需要修改xml文件，使之匹配

#coding=utf-8
import xml.etree.ElementTree as ET
import os
def modify_xml(path):
    updateTree = ET.parse(path)
    root = updateTree.getroot()
    # 修改数据值
    for object in root.findall('object'):  # 找到root节点下的所有object节点
        if object.find('name').text =='motorbike':
            object.find('name').text='motorcycle'
            print(path)

    updateTree.write(path)

if __name__ == '__main__':
    file_path='E:/datasets/VOCdevkit/VOC2012/Annotations_ssd/'
    for i in os.listdir(file_path):
        modify_xml(file_path+i)


