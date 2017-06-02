#!/usr/bin/env python2

#scrapes Supreme's store for item codes
# by Paulo Warren 3/5/17

from bs4 import BeautifulSoup
from urllib import urlopen
from datetime import datetime
import json
import time

url = 'http://www.supremenewyork.com/shop/all/'
content = urlopen(url).read()
soup = BeautifulSoup(content, 'html.parser')

with open('/var/www/html/items.json', 'r') as f:
  data = json.load(f)

add_c = 0
print('starting scan')
for img in soup.find_all('img'):

  try:
    link = img.parent.get('href')
    url = 'http://www.supremenewyork.com' + link

    specific_content = urlopen(url)
    s_soup = BeautifulSoup(specific_content, 'html.parser')

    title_split = str(s_soup.title.string.encode('ascii', errors='ignore'))[8:-1].split(' - ')

    title = title_split[0]
    color = title_split[1]
    alt = img.get('alt')

    item = {
        'title': title,
        'color': color,
        'alt': alt
        }

    if item not in data['items']:
      print('found new item ' + title + ' ' + color)
      add_c += 1
      data['items'].append(item)
    else:
      print('no new item')
    time.sleep(4)
  except:
    continue

with open('/var/www/html/items.json', 'w') as f:
  if(add_c != 0):
    data['update_time'] = datetime.now().strftime("%B %d, %H:%M %p") + ' UTC'
    
    json.dump(data, f)
    print('Scan finished, found ' + str(add_c) + ' new items and saved them')
  else:
    print('Scan finished, no new items found')
