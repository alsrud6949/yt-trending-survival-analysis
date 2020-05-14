# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 16:38:27 2019

@author: Mingyeong
"""
#after running datapreprocessing.py
import pandas as pd
import numpy as np
import os
from youtube_transcript_api import YouTubeTranscriptApi

dd = pd.read_csv('fulldata.csv')
selection = np.unique(dd['video_id'])

#captions of each video as each csv file 
os.chdir('D:\\youtube_caption')

error = []
for i in range(0,len(selection)-1):
    vid = selection[i]
    try:
        caption = YouTubeTranscriptApi.get_transcript(vid, languages=['en'])
        with open('{vid}.csv'.format(vid=vid), 'w', encoding='utf-8') as f:
            for row in caption:
                f.write("{row}\n".format(row=row))
    except Exception:
        error.append(vid)
        pass
    
error = pd.DataFrame.from_dict(error)
error.to_csv('__errorcaptionlist.csv')
 
