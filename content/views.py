from django.shortcuts import render
from rest_framework.views import APIView
from content.models import Feed, Reply, Like, Bookmark
from rest_framework.response import Response
from rest_framework.response import Response
import os
from jinstagram.settings import MEDIA_ROOT
from uuid import uuid4


class UploadFeed(APIView):
    def post(self, request):


        file = request.FILES['file']


        uuid_name = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT, uuid_name)
        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        
        content = request.data.get('content')
        image = uuid_name
        email = request.session.get('email',None)

        Feed.objects.create(content=content, image=image, email=email)
        return Response(status=200)

class UploadReply(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        reply_content = request.data.get('reply_content', None)
        email = request.session.get('email', None)

        Reply.objects.create(feed_id=feed_id, reply_content=reply_content, email=email)

        return Response(status=200)

class ToggleLike(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        favorite_text = request.data.get('favorite_text', True)
        email = request.session.get('email', None)

        if favorite_text == 'favorite_border':
            is_like = True
        else:
            is_like = False

        like = Like.objects.filter(feed_id=feed_id, email=email).first()

        if like:
            like.is_like = is_like
            like.save()
        else:
            Like.objects.create(feed_id=feed_id, is_like=is_like, email=email)

        return Response(status=200)

class ToggleBookmark(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        bookmark_text = request.data.get('bookmark_text', True)
        email = request.session.get('email', None)

        if bookmark_text == 'bookmark_border':
            is_marked = True
        else:
            is_marked = False

        bookmark = Bookmark.objects.filter(feed_id=feed_id, email=email).first()

        if bookmark:
            bookmark.is_marked = is_marked
            bookmark.save()
        else:
            Bookmark.objects.create(feed_id=feed_id, is_marked=is_marked, email=email)

        return Response(status=200)