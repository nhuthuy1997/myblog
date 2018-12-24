from .general import get_page_content, queue, stringToInt
from .models import Post, SourceInfo, Tag
from .models import TAG_COLOR
from bs4 import BeautifulSoup
from django.conf import settings
import random
from django.db.utils import IntegrityError

source = SourceInfo.objects.get(name='T')

def get_categories(content):
  nav_main = content.find_all('nav', attrs={'class':'main-nav'})[0]
  categories_list = nav_main.find_all('li')
  return categories_list

def store_tag(tag):
  name = tag.find_all('a')[0].get_text()
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
  a_tag = content.find_all('a')[0]
  title = a_tag.get_text()
  link = a_tag['href']
  hash_title = stringToInt(title)
  try:
    post = Post(source_info=source_info, title=title, link=link, hash_title=hash_title)
    post.save()
    page_content = get_page_content(link)
    if page_content[0]:
      list_tag = page_content[1].find_all('ul', attrs={'class':'post-tags-list'})[0]
      for tag in list_tag.find_all('li'):
        store_tag(tag)
    else:
      return page_content[1]
  except IntegrityError:
    return -1

def get_posts_in_category(url):
  page_content = get_page_content(url)
  if page_content[0]:
    page_content = page_content[1]
    posts = page_content.find_all('article', attrs={'class':'post'})
    for post in posts:
      post_content = post.find_all('h3')
      if len(post_content) > 0:
        store_post(post.find_all('h3')[0])
    next_page = page_content.find_all('a', attrs={'class':'pn-item'})[-1]['href']
    queue.enqueue(get_posts_in_category, next_page)
  else:
    return page_content

def process_post(url):
  page_content = get_page_content(url)
  if page_content[0]:
    categories_list = get_categories(page_content[1])
    for category in categories_list:
      queue.enqueue(get_posts_in_category, category.find_all('a')[0]['href'])
  else:
    return page_content[1]
