from os import name
from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import register, CustomLoginView, ProfileDetailView, follow_profile, search, Chat

urlpatterns = [
    path('login/', CustomLoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('register/', register, name='register'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/follow/<int:pk>', follow_profile, name='follow_profile'),
    path('results/', search, name='search'),
    path('chat/<int:profile_pk>/', Chat.as_view(), name='chat')
]