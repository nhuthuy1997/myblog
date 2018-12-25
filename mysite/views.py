from django.shortcuts import render
from crawler.models import *
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import *
import pdb

def homepage(request):
  post_list = Post.paginate(0, 10)
  all_tags = Tag.objects.all()[0:250]
  all_sources = SourceInfo.objects.all()
  source_ids = '-'.join(map(str, all_sources.values_list('id', flat=True)))
  return render(request, 'mysite/homepage.html', {'post_list': post_list, 'all_tags':all_tags, 'all_sources':all_sources, 'source_ids':source_ids})

def scroll(request, start):
  post_list = Post.paginate(int(start), int(start) + 10)
  html = render_to_string('mysite/_scroll.html', {'post_list': post_list})
  return HttpResponse(html)

def scroll_filter(request, tags, sources, start):
  sources = list(map(int, sources.split('-')))
  if tags:
    tags = list(map(int, tags.split('-')))
    post_list = Post.objects.filter(source_info_id__in = sources).prefetch_related('tags').filter(tags__hash_name__in = tags)[int(start):int(start) + 10]
  else:
    post_list = Post.objects.filter(source_info_id__in = sources).prefetch_related('tags')[int(start):int(start) + 10]
  return render(request, 'mysite/_scroll.html', {'post_list': post_list})

def filter_query(request, query):
  if request.is_ajax():
    tags = Tag.objects.filter(name__icontains = query)
    if tags:
      html = render_to_string('mysite/_filter_ajax.html', {'all_tags': tags})
    else:
      html = 'Không tìm thấy tag phù hợp'
    return HttpResponse(html)

def filter(request, tags, sources):
  sources = list(map(int, sources.split('-')))
  all_tags = Tag.objects.all()[0:250]
  all_sources = SourceInfo.objects.all()
  source_ids = '-'.join(map(str, all_sources.values_list('id', flat=True)))
  if tags:
    tags = list(map(int, tags.split('-')))
    post_list = Post.objects.filter(source_info_id__in = sources).prefetch_related('tags').filter(tags__hash_name__in = tags)[:10]
  else:
    post_list = Post.objects.filter(source_info_id__in = sources).prefetch_related('tags')[:10]
  return render(request, 'mysite/homepage.html', {'post_list': post_list, 'all_tags':all_tags, 'all_sources':all_sources, 'source_ids':source_ids})

@login_required
def favorites(request):
  post_list = Post.paginate(0, 10)
  all_tags = Tag.objects.all()[0:250]
  all_sources = SourceInfo.objects.all()
  source_ids = '-'.join(map(str, all_sources.values_list('id', flat=True)))
  return render(request, 'mysite/homepage.html', {'post_list': post_list, 'all_tags':all_tags, 'all_sources':all_sources, 'source_ids':source_ids})

@login_required
def user_logout(request):
  logout(request)
  return HttpResponseRedirect(reverse('mysite:homepage'))

def register(request):
  registered = False
  list_errors = ''
  if request.method == 'POST':
    user_form = UserForm(data=request.POST)
    password_confirm = request.POST.get('password_confirmation')
    password = request.POST.get('password')
    if user_form.is_valid():
      if password == password_confirm:
        user = user_form.save()
        user.set_password(user.password)
        user.save()
        login(request,user)
        return HttpResponseRedirect(reverse('mysite:homepage'))
      else:
        errors = 'Password not match'
    else:
      for field in user_form.fields:
        for error in user_form.errors.get(field, []):
          list_errors += error
          list_errors += '<br>'
  return render(request, 'mysite/registrator.html', {'errors':list_errors})

def user_login(request):
  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    errors = 'Email or password is invalid'
    if user:
      if user.is_active:
        login(request,user)
        return HttpResponseRedirect(reverse('mysite:homepage'))
      else:
        return render(request, 'mysite/login.html', {'errors':errors})
    else:
      return render(request, 'mysite/login.html', {'errors':errors})
  else:
    return render(request, 'mysite/login.html', {})

def search(request, query):
  post_list = Post.objects.filter(title__icontains = query)[:10]
  all_tags = Tag.objects.all()[0:250]
  all_sources = SourceInfo.objects.all()
  source_ids = '-'.join(map(str, all_sources.values_list('id', flat=True)))
  return render(request, 'mysite/homepage.html', {'post_list': post_list, 'all_tags':all_tags, 'all_sources':all_sources, 'source_ids':source_ids})

def search_pagination(request, query, start):
  post_list = Post.objects.filter(title__icontains = query)[int(start):int(start) + 10]
  html = render_to_string('mysite/_scroll.html', {'post_list': post_list})
  return HttpResponse(html)

@login_required
def clip_post(request, hash_title):
  post = Post.objects.filter(hash_title=hash_title)[0]
  user = request.user
  user_post = UserPost.objects.filter(id = int(str(post.id)+str(user.id)))
  if user_post:
    user_post[0].delete()
    messages = 'Unclipped'
  else:
    user_post = UserPost(id = int(str(post.id)+str(user.id)), post_id = post, user_id = user)
    user_post.save()
    messages = 'Clipped'
  return HttpResponse(messages)

@login_required
def clip(request):
  post_list = Post.objects.filter(id__in=UserPost.objects.filter(user_id = request.user).values_list('post_id', flat=True))
  all_tags = Tag.objects.all()[0:250]
  all_sources = SourceInfo.objects.all()
  source_ids = '-'.join(map(str, all_sources.values_list('id', flat=True)))
  return render(request, 'mysite/homepage.html', {'post_list': post_list, 'all_tags':all_tags, 'all_sources':all_sources, 'source_ids':source_ids})
