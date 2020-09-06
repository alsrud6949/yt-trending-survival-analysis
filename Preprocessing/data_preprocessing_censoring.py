# -*- coding: utf-8 -*-
"""
Data Preprocessing and Censoring
"""

import pandas as pd
import numpy as np
import glob, os
import datetime

os.chdir('D:\\data')
filenames = glob.glob('*.xlsx')
df = pd.concat( [ pd.read_excel(f) for f in filenames ] )
df.shape

#rank variable
df['rank']=df.index+1
dflist = list(df.columns)
dflist_new = dflist[-1:]+dflist[:-1]
df = df[dflist_new]

#trending_date variable
df['time'] = df['time'].apply(lambda x: str(x).zfill(4))
df['time'] = df['time'].apply(lambda x: '{H}:{M}'.format(H=x[:-2], M=x[-2:]))
df['trending_date']=df['trending_date']+' '+df['time']
df["trending_date"] = pd.to_datetime(df['trending_date'])
df["trending_date"].describe()

#select 0302~ unique video
cond = df['trending_date']>= datetime.datetime(2019,3,2)
df1 = df[cond]
df1['video_id'].describe()
selection = np.unique(df1['video_id'])

#censoring
mask = df.video_id.apply(lambda x: any(item for item in selection if item in x))
df2 = df[mask]
df2['video_id'].describe()

#replace ",","\n", "\r" to " " and string description
df2['description'] = df2['description'].apply(lambda x: str(x).replace(',', ' '))
df2['description'] = df2['description'].apply(lambda x: str(x).replace('\n', ' '))
df2['description'] = df2['description'].apply(lambda x: str(x).replace('\r', ' '))
df2['description'] = df2['description'].apply(lambda x: str(x).replace('-', ''))

#csv file
df2.to_csv('y.csv', encoding = 'utf-8', sep= ',', index = False)
dd = pd.read_csv('y.csv')
dd['video_id'].describe()


#censoring2 - addictional data for videos that stayed more after the last trending date in dataframe dd
os.chdir('D:\\youtube data')
filenames = glob.glob('*.xlsx')
df = pd.concat( [ pd.read_excel(f) for f in filenames ] )

df['rank']=df.index+1
dflist = list(df.columns)
dflist_new = dflist[-1:]+dflist[:-1]
df = df[dflist_new]

df['time'] = df['time'].apply(lambda x: str(x).zfill(4))
df['time'] = df['time'].apply(lambda x: '{H}:{M}'.format(H=x[:-2], M=x[-2:]))
df['trending_date']=df['trending_date']+' '+df['time']
df["trending_date"] = pd.to_datetime(df['trending_date'])
df["trending_date"].describe()

df['description'] = df['description'].apply(lambda x: str(x).replace(',', ' '))
df['description'] = df['description'].apply(lambda x: str(x).replace('\n', ' '))
df['description'] = df['description'].apply(lambda x: str(x).replace('\r', ' '))
df['description'] = df['description'].apply(lambda x: str(x).replace('-', ''))

newselection = np.unique(dd['video_id'])

#only select data for unique videos in dataframe dd 
mask1 = df.video_id.apply(lambda x: any(item for item in newselection if item in x))
newdf = df[mask1]
finaldf = pd.concat([dd, newdf], ignore_index=True)

finaldf.to_csv('fulldata.csv', encoding = 'utf-8', sep= ',', index = False)
