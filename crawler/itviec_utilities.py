from .general import get_page_content, queue, stringToInt
from .models import Post, SourceInfo, Tag
from .models import TAG_COLOR
from bs4 import BeautifulSoup
from django.conf import settings
import random
from django.db.utils import IntegrityError

source = SourceInfo.objects.get(name='I')

def store_tag(tag):
  name = tag.get_text()
  color = random.choice(TAG_COLOR)[0]
  hash_name = stringToInt(name)
  try:
    tag = Tag(name=name, color=color, hash_name=hash_name)
    tag.save()
    return tag
  except IntegrityError:
    return Tag.objects.filter(hash_name=hash_name)[0]

def store_post(content):
  source_info = source
  a_tag = content.find_all('h2', attrs={'class':'title'})[0].find_all('a')[0]
  title = a_tag.get_text()
  link = a_tag['href']
  hash_title = stringToInt(title)
  try:
    post = Post(source_info=source_info, title=title, link=link, hash_title=hash_title)
    post.save()
    for tag in content.find_all('a', attrs={'rel':'tag'}):
      post.tags.add(store_tag(tag))
  except IntegrityError:
    return -1
  

def process_post(url):
  page_content = get_page_content(url)
  if page_content[0]:
    page_content = page_content[1]
    next_page = page_content.find_all('a', attrs={'class':'next'})
    if len(next_page)==0:
      return 1
    else:
      for post in page_content.find_all('div', attrs={'class':'post'}):
        store_post(post)
      url = next_page[0]['href']
      queue.enqueue(process_post, url)
  else:
    return page_content[1]
