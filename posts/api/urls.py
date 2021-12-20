from django.urls import path

from .api_view import (PostsList, PostDetail, CreatePost,
                       LikePost, UnlikePost)


urlpatterns = [
    path('posts/', PostsList.as_view(), name='posts'),
    path('posts/<int:id>/', PostDetail.as_view(), name='post'),
    path('posts/create/', CreatePost.as_view(), name='create'),

    path('posts/<int:id>/like/', LikePost.as_view(), name='like'),
    path('posts/<int:id>/unlike/', UnlikePost.as_view(), name='unlike'),
]
