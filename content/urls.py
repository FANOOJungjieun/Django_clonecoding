from django.urls import path
from .views import UploadFeed, UploadReply, ToggleLike, ToggleBookmark

urlpatterns = [
    path('upload', UploadFeed.as_view(), name='upload_feed'),
    path('reply', UploadReply.as_view()),
    path('like', ToggleLike.as_view()),
    path('bookmark', ToggleBookmark.as_view()),
]