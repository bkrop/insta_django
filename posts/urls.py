from os import name
from django.urls import path
from .views import PostCreateView, PostDetailView, PostListView, hashtag_posts

urlpatterns = [
    path('create/', PostCreateView.as_view(), name='create_post'),
    path('<int:pk>/', PostDetailView.as_view(), name='detail_post'),
    path('home/', PostListView.as_view(), name='homepage'),
    path('hashtag/<str:hashtag>/', hashtag_posts, name='hashtag_posts')
]
