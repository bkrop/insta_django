from os import name
from django.urls import path
from .views import PostCreateView, PostDetailView, PostListView, hashtag_posts, like_post

urlpatterns = [
    path('create/', PostCreateView.as_view(), name='create_post'),
    path('<int:pk>/', PostDetailView.as_view(), name='detail_post'),
    path('home/', PostListView.as_view(), name='homepage'),
    path('hashtag/<str:hashtag>/', hashtag_posts, name='hashtag_posts'),
    path('like/<int:post_id>/', like_post, name='like_post')
]
