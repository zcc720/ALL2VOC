# -*- coding: utf-8 -*-
# @Time    : 2018/12/25 13:50
# @Author  : zcc
# @File    : kitti2voc.py
# @Function:

import glob


txt_list = glob.glob('E:/datasets/kitti/data_object_label_2/training/label_2/*.txt') # 存储Labels文件夹所有txt文件路径
print(txt_list)
def show_category(txt_list):
    category_list= []
    for item in txt_list:
        try:
            with open(item) as tdf:
                for each_line in tdf:
                    labeldata = each_line.strip().split(' ') # 去掉前后多余的字符并把其分开
                    category_list.append(labeldata[0]) # 只要第一个字段，即类别
        except IOError as ioerr:
            print('File error:'+str(ioerr))
    print(set(category_list)) # 输出集合
show_category(txt_list)

def merge(line):
    each_line=''
    for i in range(len(line)):
        if i!= (len(line)-1):
            each_line=each_line+line[i]+' '
        else:
            each_line=each_line+line[i] # 最后一条字段后面不加空格
    each_line=each_line+'\n'
    return (each_line)

print('before modify categories are:\n')
show_category(txt_list)

for item in txt_list:
    new_txt=[]
    try:
        with open(item, 'r') as r_tdf:
            for each_line in r_tdf:
                labeldata = each_line.strip().split(' ')
                labeldata[4] = str(int(float(labeldata[4])))
                labeldata[5] = str(int(float(labeldata[5])))
                labeldata[6] = str(int(float(labeldata[6])))
                labeldata[7] = str(int(float(labeldata[7])))
                if labeldata[0] in ['Van','Car']: # 合并汽车类
                    labeldata[0] = labeldata[0].replace(labeldata[0],'car')
                if labeldata[0] in ['DontCare', 'Misc','Person_sitting']: # 合并这三类用于忽略
                    labeldata[0] = labeldata[0].replace(labeldata[0], 'dontcare')
                if labeldata[0] in ['Pedestrian','Cyclist'] :  # 合并行人类
                    labeldata[0] = labeldata[0].replace(labeldata[0], 'person')
                if labeldata[0] =='Truck':
                    labeldata[0] = labeldata[0].replace(labeldata[0], 'truck')
                if labeldata[0] !='Tram':
                    new_txt.append(merge(labeldata)) # 重新写入新的txt文件
        with open(item,'w+') as w_tdf: # w+是打开原文件将内容删除，另写新内容进去
            for temp in new_txt:
                w_tdf.write(temp)
    except IOError as ioerr:
        print('File error:'+str(ioerr))

print('\nafter modify categories are:\n')
show_category(txt_list)