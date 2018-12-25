# -*- coding: utf-8 -*-
# @Time    : 2018/12/21 10:02
# @Author  : zcc
# @File    : OpenImageV4_to_voc.py
# @Function:

import pandas as pd
import numpy as np
import os
import tensorflow as tf
import io
import logging
import random
import PIL.Image
from PIL import ImageDraw
import hashlib
import urllib
import matplotlib.pyplot as plt

class open_image_dataset:
    '''
    图片表描述图片信息，最重要是下载地址，
    边界框表主要描述一张图有几个边框，它与图片表通过外键ImageID关联，
    同时每个边框具体属于哪个分类，又要通过LabelName外键和标签表关联。
    '''
    #标签表
    classname_csv = "https://storage.googleapis.com/openimages/2018_04/class-descriptions-boxable.csv"

    test_image_csv = "https://storage.googleapis.com/openimages/2018_04/test/test-images-with-rotation.csv"
    test_box_csv = "https://storage.googleapis.com/openimages/2018_04/test/test-annotations-bbox.csv"

    val_image_csv = "https://storage.googleapis.com/openimages/2018_04/validation/validation-images-with-rotation.csv"
    val_box_csv = "https://storage.googleapis.com/openimages/2018_04/validation/validation-annotations-bbox.csv"

    train_image_csv = "https://storage.googleapis.com/openimages/2018_04/train/train-images-boxable-with-rotation.csv"
    train_box_csv = "https://storage.googleapis.com/openimages/2018_04/train/train-annotations-bbox.csv"

    def download_test(self):
        print('start download test info')
        folder='test'
        if not os.path.exists(folder):
            os.mkdir(folder)
            image_csv_path=folder+'/image.csv'
            box_csv_path=folder+'/box.csv'
            classname_csv_path=folder+'/classname.csv'
            if os.path.exists(image_csv_path) is False:
                urllib.request.urlretrieve(self.test_image_csv,image_csv_path)
            if os.path.exists(box_csv_path) is False:
                urllib.request.urlretrieve(self.test_box_csv,box_csv_path)
            if os.path.exists(classname_csv_path) is False:
                urllib.request.urlretrieve(self.classname_csv,classname_csv_path)
            print('down test complete')

    def create_tfrecord(self,folder,keywords):
        image_csv_path = folder + "/image.csv"
        box_csv_path = folder + "/box.csv"
        classname_csv_path = folder + "/classname.csv"

        df_image = pd.read_csv(image_csv_path)
        df_box = pd.read_csv(box_csv_path)
        df_classname = pd.read_csv(classname_csv_path, names=['labelID', 'LabelName'])

        data = df_classname[df_classname['LabelName'] == keywords]
        data = pd.merge(data, df_box, left_on='labelID', right_on='LabelName', how='right')
        data = pd.merge(data, df_image, left_on='ImageID', right_on='ImageID', how='right')
        # print(data)
        data = data[data['labelID'].notnull() & data['ImageID'].notnull()]
        folder_path = keywords + "/" + folder + "/"
        if os.path.exists(folder_path) is False:
            os.makedirs(folder_path)
        for index, row in data.iterrows():
            objs=[]
            file_name = row['ImageID'] + ".jpg"
            file_path = folder_path + file_name
            if os.path.exists(file_path) is False:
                try:
                    urllib.request.urlretrieve(row['OriginalURL'], file_path)
                except urllib.error.HTTPError as e:
                    print('打不开！哼')
                    continue
                except urllib.error.URLError as e:
                    print('打不开！哼')
                    continue
                except Exception as e:
                    print('打不开！哼')
                    continue

            image = PIL.Image.open(file_path)
            width = image.width
            height = image.height
            if image.format != 'JPEG':
                print("file format error " + file_path)
                os.remove(file_path)
                continue
            xmin=(int(width*float(row['XMin'])))
            xmax=(int(width*float(row['XMax'])))
            ymin=(int(height*float(row['YMin'])))
            ymax=(int(height*float(row['YMax'])))
            obj = [file_name, str(xmin), str(ymin), str(xmax), str(ymax)]
            s=' '.join(obj)
            return s



dataset=open_image_dataset()
dataset.download_test()
dataset.create_tfrecord('test','Truck')










