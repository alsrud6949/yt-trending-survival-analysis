# -*- coding: utf-8 -*-
"""
Video Thumbnail Image Extraction
"""

from urllib.request import urlretrieve
import os
import filetype
import pandas as pd
import numpy as np

os.chdir('D:\\youtube data')
df=pd.read_csv('fulldata.csv')

img_list=np.unique(df['thumbnail_link'].values.tolist())
filename = np.unique(df['video_id'].values.tolist())

os.chdir("D:\\thumbnail_image")
for i in range(len(img_list)):
    name = filename[i]
    # download image from link
    urlretrieve(img_list[i],name)
    # image extension
    ext = ".jpg"
    # rename the image file as {video id}.jpg
    os.rename(name, name + ext)
