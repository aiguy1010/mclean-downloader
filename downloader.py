import requests
import re
import os

# Compile some useful Regular Expressions
titlePattern = re.compile('<item>.*?<title>(.*?)<\/title>', re.DOTALL)
sermonUrlPattern = re.compile('<item>.*?<link>(.*?)<\/link>', re.DOTALL)
contentUrlPattern = re.compile('<meta property="og:video" content="(.*?)\?')

# Request the McLean RSS feed and pull the some info from it
print('Fetching Sermons...')
rss = requests.get('https://www.mcleanbible.org/sermons/rss.xml')
titles = titlePattern.findall(rss.text)
sermonUrls = sermonUrlPattern.findall(rss.text)

# Find out which item the user wants to download
print('Sermons Fetched:')
for n in range(len(titles)):
	# Before printing, try to avoid a specific error that has been occuring
	titles[n] = titles[n].replace('\u2019', '\'')

	# Also, get rid of that pesky "(Video)" tag if it's there
	titles[n]=titles[n].replace('(Video)', '').strip()

	print( '{0:>2}. {1}'.format(n+1,titles[n]) )
sermonUrl = ''
title = ''
while True:
	try:
		n=int(input('\nPlease enter the number of the item you would like to download.\n>'))
		sermonUrl = sermonUrls[n-1]
		title = titles[n-1]
	except Exception:
		print('Sorry, count not understand that input...')
		continue
	break

# Request the sermon page and pull the link to the content from it
sermonPage = requests.get(sermonUrl)
contentUrl = contentUrlPattern.search(sermonPage.text).group(1)

# Generate a filename from content title
exemptions = ' -_()'
filename = ''.join(c for c in title if c.isalnum() or c in exemptions)

# Use VLC to download and save the content as an audio file
print('Downloading and Converting...')
vlcCmd = 'vlc'
vlcSuffix = '--sout=#transcode{acodec=mp3,vcodec=dummy}:standard{access=file,mux=raw,dst=".\\Downloads\\'+filename+'.mp3"} vlc://quit'
os.system(vlcCmd + ' '+contentUrl+' ' + vlcSuffix)
print('Done.')
