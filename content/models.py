from django.db import models

# Create your models here.

class Feed(models.Model):
    content       = models.TextField() # 본문
    image         = models.TextField() # 사진
    email         = models.EmailField(default='')     # 글쓴이. 이 값으로 프로필 이미지와 아이디를 찾아온다.

class Like(models.Model):
    feed_id = models.IntegerField(default=0)
    email = models.EmailField(default='')
    is_like = models.BooleanField(default=True)

class Reply(models.Model):
    feed_id = models.IntegerField(default=0)
    email = models.EmailField(default='')
    reply_content = models.TextField()

class Bookmark(models.Model):
    feed_id = models.IntegerField(default=0)
    email = models.EmailField(default='')
    is_marked = models.BooleanField(default=True)