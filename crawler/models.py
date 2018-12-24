from django.db import models
from django.contrib.auth.models import User
from background_task import background
from datetime import timedelta

POST_STATUS = (
  ('N', 'New'),
  ('W', 'Warning'),
  ('R', 'Reject'),
  ('P', 'Publish'),
)

SOURCE_NAME = (
  ('U', 'Unknown'),
  ('V', 'Viblo'),
  ('T', 'TechBlog'),
  ('I', 'ITviec'),
  ('J', 'JamViet'),
)

TAG_COLOR = (
  ('Gray', 'default'),
  ('Blue', 'primary'),
  ('Green', 'success'),
  ('Light Blue', 'info'),
  ('Orange', 'warning'),
  ('Red', 'danger'),
)

TAG_STATUS = (
  ('N', 'New'),
  ('W', 'Warning'),
  ('R', 'Reject'),
  ('P', 'Publish'),
)

class SourceInfo(models.Model):
  name = models.CharField(max_length=1, choices=SOURCE_NAME, default=SOURCE_NAME[0][0], unique=True)
  image = models.CharField(max_length=190, default='')
  description = models.TextField(max_length=500, default='')

class Tag(models.Model):
  name = models.CharField(max_length=190)
  color = models.CharField(max_length=15, choices=TAG_COLOR, default=TAG_COLOR[0][0])
  hash_name = models.BigIntegerField(unique=True, default=0, db_index=True)
  status = models.CharField(max_length=1, choices=POST_STATUS, default=TAG_STATUS[0][0])

class Post(models.Model):
  status = models.CharField(max_length=1, choices=POST_STATUS, default=POST_STATUS[0][0])
  source_info = models.ForeignKey(SourceInfo, on_delete=models.CASCADE)
  title =  models.TextField(max_length=500, default='')
  link = models.CharField(max_length=190, default='')
  view_count = models.IntegerField(default=0)
  sentences_of_summary = models.IntegerField(default=5)
  summary = models.TextField(max_length=2500, default='')
  hash_title = models.BigIntegerField(unique=True, default=0, db_index=True)
  tags = models.ManyToManyField(Tag)

  def is_not_exists(self):
    return Post.objects.get(hash_title=self.hash_title) is None

  def check_status():
    for post in Post.objects.all():
      if '' in post.title:
        post.status = 'W'
        post.save()
        post.auto_approve()

  @background(schedule=timedelta(days=3))
  def auto_approve(self, status):
    self.status = status
    self.save()
