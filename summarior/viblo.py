from crawler.general import get_page_content
from functools import reduce
from crawler.models import *


def get_paragraph(url):
  try:
    content = get_page_content(url)[1]
    for blockquote in content.find_all('blockquote'):
      blockquote.decompose()
    content = content.find_all('article', attrs={'class':'post-content'})[0].find_all('p')
    content[0] = content[0].get_text()
    return reduce(lambda x, y: x + y.get_text(), content).replace('\n', '.')
  except:
    return 'fail: ' + url
