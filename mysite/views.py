from django.shortcuts import render
from .models import *
from django.shortcuts import render

def homepage(request):
  post_list = Post.objects.filter(status='P')
  return render(request, 'mysite/homepage.html', {'post_list': post_list})
