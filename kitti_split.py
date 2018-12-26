# -*- coding: utf-8 -*-
# @Time    : 2018/12/26 15:31
# @Author  : zcc
# @File    : kitti_split.py
# @Function:
import os
import shutil
import cv2
import glob

headstr = """\
<annotation>
    <folder>KITTI</folder>
    <filename>%s</filename>
    <source>
        <database>My Database</database>
        <annotation>KITTI</annotation>
        <image>flickr</image>
        <flickrid>NULL</flickrid>
    </source>
    <owner>
        <flickrid>NULL</flickrid>
        <name>company</name>
    </owner>
    <size>
        <width>%d</width>
        <height>%d</height>
        <depth>%d</depth>
    </size>
    <segmented>0</segmented>
"""
objstr = """\
    <object>
        <name>%s</name>
        <pose>Unspecified</pose>
        <truncated>0</truncated>
        <difficult>0</difficult>
        <bndbox>
            <xmin>%d</xmin>
            <ymin>%d</ymin>
            <xmax>%d</xmax>
            <ymax>%d</ymax>
        </bndbox>
    </object>
"""

tailstr = '''\
</annotation>
'''

txt_path='E:/datasets/kitti/data_object_label_2/training/label_2/'
img_path='E:/datasets/kitti/data_object_image_2/training/image_2/'
img_savedir='E:/datasets/kitti/JPEGImages/'
anno_savedir='E:/datasets/kitti/Annotations/'
def mkr(path):
    if os.path.exists(path):
        shutil.rmtree(path)
        os.mkdir(path)
    else:
        os.mkdir(path)
mkr(img_savedir)
mkr(anno_savedir)

def read_txt_and_handle_image(txt_path):
    image_path = img_path + txt_path.split('\\')[-1].split('.')[0] + '.jpg'
    img = cv2.imread(image_path)
    h,w,c=img.shape
    saveimg = img.copy()
    img_left=saveimg[0:h, 0:int(w/2), :]
    img_left_filename=txt_path.split('\\')[-1].split('.')[0] + '_left_kitti.jpg'
    img_right=saveimg[0:h,int(w/2):w,:]
    img_right_filename=txt_path.split('\\')[-1].split('.')[0] + '_right_kitti.jpg'

    left_objects = []
    right_objects=[]
    with open(txt_path) as tdf:
        for each_line in tdf:
            line_data = each_line.strip().split(' ')  # 去掉前后多余的字符并把其分开
            class_name = line_data[0]
            xmin = int(line_data[4])
            ymin = int(line_data[5])
            xmax = int(line_data[6])
            ymax = int(line_data[7])
            obj_left = [class_name, xmin, ymin , xmax, ymax]
            obj_right=[class_name, xmin-int(w/2), ymin , xmax-int(w/2), ymax]
            #在左图的有效框
            if xmax<=int(w/2):
                if class_name in ['car','person','truck']:
                    left_objects.append(obj_left)
                else:
                    img_left[ymin:ymax, xmin:xmax, :] = (104, 117, 123)
            #右图有效框
            if xmin>=int(w/2):
                if class_name in ['car','person','truck']:
                    right_objects.append(obj_right)
                else:
                    img_right[ymin:ymax, xmin-int(w/2):xmax-int(w/2), :] = (104, 117, 123)
            if xmin<int(w/2) and xmax>int(w/2):
                img_left[ymin:ymax, xmin:int(w/2), :] = (104, 117, 123)
                img_right[ymin:ymax, 0:xmax-int(w/2), :]=(104, 117, 123)
    if len(left_objects) !=0:
        cv2.imwrite(img_savedir + img_left_filename, img_left)
    if len(right_objects) !=0:
        cv2.imwrite(img_savedir + img_right_filename, img_right)

    return left_objects,right_objects,img_left_filename,img_right_filename,h,w,c

def write_xml(anno_path,head, objs, tail):
    f = open(anno_path, "w")
    f.write(head)
    for obj in objs:
        f.write(objstr%(obj[0],obj[1],obj[2],obj[3],obj[4]))
    f.write(tail)

txt_list = glob.glob(txt_path+'*.txt')
for txt in txt_list:
    left_objects,right_objects,img_left_filename,img_right_filename,h,w,c=read_txt_and_handle_image(txt)
    xml_left_filename = anno_savedir+txt.split('\\')[-1].split('.')[0] + '_left_kitti.xml'
    xml_right_filename = anno_savedir+txt.split('\\')[-1].split('.')[0] + '_right_kitti.xml'

    if len(left_objects)!=0:
        head = headstr % (img_left_filename, int(w/2), h, c)
        write_xml(xml_left_filename, head, left_objects, tailstr)
    if len(right_objects)!=0:
        head = headstr % (img_right_filename, int(w/2), h, c)
        write_xml(xml_right_filename, head, right_objects, tailstr)
    print(left_objects)