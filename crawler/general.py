from bs4 import BeautifulSoup as bs
import requests
import django_rq
import redis
from urllib3.exceptions import ReadTimeoutError, NewConnectionError
import hashlib

queue = django_rq.get_queue('default')

def get_page_content(url):
  try:
    page_response = requests.get(url, timeout=5)
    return [True, bs(page_response.content, 'html.parser')]
  except ReadTimeoutError:
    return [False, 'request timeout']
  except NewConnectionError:
    return [False, 'can\'t reach this URL']

def stringToInt(mstr):
  return int(hashlib.md5(mstr.encode()).hexdigest(), 16) % 10**16
