from os import name
from django.urls import path
from .views import (
    PostCreateView,
    PostDetailView,
    hashtag_posts,
    like_post,
    PostUpdateView,
    post_comments,
    homepage
)

urlpatterns = [
    path('create/', PostCreateView.as_view(), name='create_post'),
    path('<int:pk>/', PostDetailView.as_view(), name='detail_post'),
    path('home/', homepage, name='homepage'),
    path('hashtag/<str:hashtag>/', hashtag_posts, name='hashtag_posts'),
    path('like/<int:post_id>/', like_post, name='like_post'),
    path('update/<int:pk>/', PostUpdateView.as_view(), name='update_post'),
    path('comments/<int:pk>/', post_comments, name='post_comments')
]
