# -*- coding: utf-8 -*-
"""
Created on Mon May 11 22:49:09 2020

@author: Mingyeong
"""

import requests, sys, time

snippet_features = ["title",
                    "publishedAt",
                    "channelTitle",
                    "categoryId"]

header = ["video_id"] + ["trending_date"] +["time"] + ['channelId'] + snippet_features + ['subscriber_count'] + ['video_count'] + ["thumbnail_link"
         , "duration", "caption", "licensedContent", "projection" 
         , "comments_disabled", "ratings_disabled", "view_count", "likes", "dislikes"
         , "comment_count", "tags", "description"]

unsafe_characters = ['\n', '"']

def prepare_feature(feature):
    # Removes any character from the unsafe characters list and surrounds the whole item in quotes
    for ch in unsafe_characters:
        feature = str(feature).replace(ch,"")
    return '"{feature}"'.format(feature=feature)

def get_tags(tags_list):
    # Takes a list of tags, prepares each tag and joins them into a string by the pipe character
    return prepare_feature("|".join(tags_list))


request_url = """
https://www.googleapis.com/youtube/v3/videos?
part=id,statistics,contentDetails,status,snippet
&chart=mostPopular&regionCode=US
&maxResults=50
&key={my YouTube Data API key}
"""
request = requests.get(request_url)
if request.status_code == 429:
    print("Temp-Banned due to excess requests, please wait and continue later")
    sys.exit()
    
video_info = request.json()

def get_videos(items):
    lines = []
    for video in items:
        comments_disabled = False
        ratings_disabled = False
        
        if "statistics" not in video:
            continue
        
        video_id = prepare_feature(video['id'])
        
        snippet = video['snippet']
        statistics = video['statistics']
        contentDetails = video['contentDetails']

        channelId = snippet.get('channelId','')
        features = [prepare_feature(snippet.get(feature, "")) for feature in snippet_features]
        
        request_url2 = """
        https://www.googleapis.com/youtube/v3/channels?
        part=statistics&id={channelId}
        &key={my YouTube Data API key}
        """
        channel = request_url2.replace("{channelId}",channelId)
        request2 = requests.get(channel)
        if request2.status_code == 429:
             print("Temp-Banned due to excess requests, please wait and continue later")
             sys.exit()
        ch_info = request2.json()
        ch_item = ch_info['items'][0]
        ch_stat = ch_item['statistics']
        subscriberCount = ch_stat['subscriberCount']
        videoCount = ch_stat['videoCount']
        
        description = snippet.get("description", "")
        thumbnail_link = snippet.get("thumbnails", dict()).get("high", dict()).get("url", "")
        trending_date = time.strftime("%Y-%m-%d")
        trending_time = time.strftime("%H%M")
        tags = get_tags(snippet.get("tags", ["[none]"]))
        view_count = statistics.get("viewCount", 0)
        duration = contentDetails.get("duration")
        caption = contentDetails.get("caption")
        licensedContent = contentDetails.get("licensedContent")
        projection = contentDetails.get("projection")
        
        if 'likeCount' in statistics and 'dislikeCount' in statistics:
            likes = statistics['likeCount']
            dislikes = statistics['dislikeCount']
        else:
            ratings_disabled = True
            likes = 0
            dislikes = 0
        
        if 'commentCount' in statistics:
            comment_count = statistics['commentCount']
        else:
            comments_disabled = True
            comment_count = 0
        
        line = [video_id] + [trending_date] + [trending_time] + [channelId] + features + [subscriberCount]+ [videoCount] + [prepare_feature(x) for x in [thumbnail_link
           , duration, caption, licensedContent, projection, comments_disabled, ratings_disabled, view_count, likes, dislikes, comment_count
           , tags, description]]
        
        lines.append(",".join(line))
    return lines

items = video_info.get('items', [])
country_data = []
country_data += get_videos(items)
country_data = [",".join(header)] + country_data

date_time = time.strftime("%m%d_%H%M")
with open("{date_time}.csv".format(date_time=date_time), "w+", encoding='utf-8') as file:
        for row in country_data:
            file.write("{row}\n".format(row=row))