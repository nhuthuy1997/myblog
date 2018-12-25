from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Post, SourceInfo, Tag
import django_rq
import redis
from . import general
from . import viblo_utilities, techblog_utilities, jamviet_utilities, itviec_utilities

import pdb

# queue = django_rq.get_queue('default')

# job = queue.enqueue(get_page_content, 'https://viblo.asia')

@login_required
def viblo(request):
  page_content = viblo_utilities.process_post(settings.VIBLO_URL)
  return page_content

@login_required
def techblog(request):
  page_content = techblog_utilities.process_post(settings.TECHBLOG_URL)
  return page_content

@login_required
def jamviet(request):
  page_content = jamviet_utilities.process_post(settings.JAMVIET_URL)
  return page_content

@login_required
def itviec(request):
  page_content = itviec_utilities.process_post(settings.ITVIEC_URL)
  return page_content
