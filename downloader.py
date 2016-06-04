import requests
import re
import os

# Compile some useful Regular Expressions
titlePattern = re.compile('<item>.*?<title>(.*?)<\/title>', re.DOTALL)
sermonUrlPattern = re.compile('<item>.*?<link>(.*?)<\/link>', re.DOTALL)
contentUrlPattern = re.compile('<meta property="og:video" content="(.*?)\?')

# Request the McLean RSS feed and pull the some info from it
print('Determining latest sermon...')
rss = requests.get('https://www.mcleanbible.org/sermons/rss.xml')
title = titlePattern.search(rss.text).group(1)
sermonUrl = sermonUrlPattern.search(rss.text).group(1)
print(title)

# Request the sermon page and pull the link to the content from it
sermonPage = requests.get(sermonUrl)
contentUrl = contentUrlPattern.search(sermonPage.text).group(1)

# Use VLC to download and save the content as an audio file
print('Downloading and Converting...')
vlcCmd = 'vlc'
vlcSuffix = '--sout=#transcode{acodec=mp3,vcodec=dummy}:standard{access=file,mux=raw,dst=".\\Downloads\\'+title+'.mp3"} vlc://quit'
os.system(vlcCmd + ' '+contentUrl+' ' + vlcSuffix)
print('Done.')
