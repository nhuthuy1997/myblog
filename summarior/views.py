from . import summarior
from crawler.models import *
from crawler.general import queue

def summary():
  for post in Post.objects.all():
    if not post.summary and post.source_info.name == 'V' and not post.has_summary:
      queue.enqueue(summarior.exec, post, summarior.get_paragraph(post.link))
