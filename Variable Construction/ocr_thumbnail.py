# -*- coding: utf-8 -*-
"""
OCR - thumbnail images
"""

import pandas as pd
import os
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
#chrome_options.add_argument('headless')
chrome_options.add_argument("---window-size=380,520")
#chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
chrome_options.add_argument("--disable-gpu")
#chrome_options.add_argument("--disable-web-security")
#chrome_options.add_argument("--disable-site-isolation-trials")
#chrome_options.add_argument("--blink-settings=imagesEnabled=false")

driver = webdriver.Chrome('./chromedriver.exe', chrome_options=chrome_options)
driver.implicitly_wait(3)
url = "https://azure.microsoft.com/en-us/services/cognitive-services/computer-vision/"
driver.get(url)

os.chdir('D:\\youtube')
data=pd.read_csv("fulldata.csv")

thumbnail_text = pd.DataFrame(columns = ["video_id","th_text"])

imgurl_form = "https://img.youtube.com/vi/<insert-youtube-video-id-here>/maxresdefault.jpg"
video_id = data.video_id.unique()
       
for i in range(len(video_id)):
    vid=video_id[i]
    imgurl = imgurl_form.replace("<insert-youtube-video-id-here>",vid)
    url_input = driver.execute_script('return document.querySelector("form[action*=ocrapi]").querySelector("input[type=text]");')
    submit_btn = driver.execute_script('return document.querySelector("form[action*=ocrapi]").querySelector("input[type=submit]");')   
    url_input.send_keys(imgurl)
    submit_btn.click()
    time.sleep(1)
    WebDriverWait(driver, 10) \
        .until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".wa-loading-progress-container")))
    time.sleep(1)
    ocr_text = driver.find_element_by_id("readTextPreview").text
    Dict = dict(  zip(thumbnail_text.columns, [vid, ocr_text])  )
    thumbnail_text = thumbnail_text.append(Dict, ignore_index=True)

thumbnail_text['th_text'] = thumbnail_text['th_text'].apply(lambda x: str(x).replace(',',' '))
thumbnail_text['th_text'] = thumbnail_text['th_text'].apply(lambda x: str(x).replace('\n',' '))
thumbnail_text['th_text'] = thumbnail_text['th_text'].apply(lambda x: str(x).replace('\r',' '))
       
# 2 types of exceptions
excep = thumbnail_text[thumbnail_text['th_text']=='We could not detect any words in the image.']
excep.iloc[:,1] = ''
excep2 = thumbnail_text[thumbnail_text['th_text']=='We were unable to pull an image at the specified url. Please try again.']
excep2.iloc[:,1] = ''

a = thumbnail_text[thumbnail_text['th_text']!='We could not detect any words in the image.']
b = a[a['th_text']!='We were unable to pull an image at the specified url. Please try again.']
concated = pd.concat([b, excep, excep2])

text = data[['video_id','title']]

data_text = pd.merge(text, concated, on = "video_id")
data_text.to_csv("ocr.csv", index = False)
