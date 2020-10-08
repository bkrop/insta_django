from os import name
from django.urls import path
from .views import PostCreateView, PostDetailView

urlpatterns = [
    path('create/', PostCreateView.as_view(), name='create_post'),
    path('<int:pk>/', PostDetailView.as_view(), name='detail_post'),
]
