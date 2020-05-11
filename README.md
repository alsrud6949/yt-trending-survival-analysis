# YouTube_Trending_Scrapper
> YouTube Trending list is updated every 15 minutes. For my thesis, I have collected data from YouTube Trending.

# Motivation
Videos in the Trending list are recognized as "most popular now contents" by YouTube algorithm. I wanted to know how these videos keep its popularity further.

# API
YouTube Data API V3
How to get credential key: https://console.developers.google.com/ > library > youtube data api v3 > Enable > Create credentials > API key
-> use as {my YouTube Data API key} in YouTube_Trending_scrapper.py

# Features
Video Information: 
video_id, pubilshed_time, title, description, thumbnails(high-resolution), channel_id, channel_title, category_id, duration, caption(True/False), licensedContent(True/False), projection(ex. Rectangular), viewCount, likeCount, dislikeCount, commentCount
Channel Information: 
subscriberCount, videoCount
