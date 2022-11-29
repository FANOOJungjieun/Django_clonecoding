import os
from uuid import uuid4
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.views import APIView

from content.models import Feed, Reply, Like, Bookmark
from user.models import User
from .settings import MEDIA_ROOT


class Main(APIView):
    def get(self, request):
        email = request.session.get('email', None)

        if email is None:
            return render(request, 'user/login.html')

        user = User.objects.filter(email=email).first()
        print(user.user_id)
        if user is None:
            return render(request, 'user/login.html')

        feed_object_list = Feed.objects.all().order_by('-id')
        feed_list = []

        for feed in feed_object_list:
            user2 = User.objects.filter(email=feed.email).first()
            reply_object_list = Reply.objects.filter(feed_id=feed.id)
            reply_list = []

            for reply in reply_object_list:
                user1 = User.objects.filter(email=reply.email).first()
                reply_list.append(dict(reply_content = reply.reply_content,
                                             user_id = user1.user_id))

            like_count=Like.objects.filter(feed_id=feed.id, is_like=True).count()
            is_liked=Like.objects.filter(feed_id=feed.id, email=email, is_like=True).exists()
            is_marked=Bookmark.objects.filter(feed_id=feed.id, email=email, is_marked=True).exists()

            feed_list.append(dict(image = feed.image,
                                content = feed.content,
                                profile_image = user2.thumbnail,
                                user_id = user2.user_id,
                                like_count=like_count,
                                reply_list=reply_list,
                                is_liked=is_liked,
                                is_marked=is_marked,
                                id = feed.id,
                                ))
        return render(request,
                    'jinstagram/main.html',
                     context=dict(feed_list=feed_list,
                                user=user))


class Profile(APIView):
    def get(self, request):
        email = request.session.get('email', None)
        if email is None:
            return render(request, 'user/login.html')

        user = User.objects.filter(email=email).first()
        if user is None:
            return render(request, 'user/login.html')

        feed_list = Feed.objects.filter(email=email)
        like_list = list(Like.objects.filter(email=email, is_like=True).values_list('feed_id', flat=True))
        like_feed_list = Feed.objects.filter(id__in=like_list) # __in : like_list in id인 모든 id리스트
        bookmark_list = list(Bookmark.objects.filter(email=email, is_marked=True).values_list('feed_id', flat=True))
        bookmark_feed_list = Feed.objects.filter(id__in=bookmark_list)

        feed_count = len(feed_list)

        return render(request,
                    'jinstagram/profile.html',
                    context=dict(feed_list=feed_list,
                                like_feed_list=like_feed_list,
                                bookmark_feed_list=bookmark_feed_list,
                                feed_count=feed_count,
                                user=user))

