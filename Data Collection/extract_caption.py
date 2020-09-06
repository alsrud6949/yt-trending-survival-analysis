# -*- coding: utf-8 -*-
"""
Video Caption (Script) Extraction
"""
import pandas as pd
import numpy as np
import os
from youtube_transcript_api import YouTubeTranscriptApi

os.chdir('D:\\youtube')
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

import glob, os

filenames = glob.glob('*.txt')

caption_list = []
        
for f in filenames:
    with open(f, 'rt', encoding='UTF8') as df:
        cap  = df.read()
    caption_list.append((f,cap))
    cc = pd.DataFrame(caption_list, columns=['filename', 'caption'])
  
cc['video_id'] = cc['filename'].apply(lambda x: '{vid}'.format(vid=x[:-4]))

os.chdir('D:\\youtube')
cc.to_csv('caption.csv', index = False)
