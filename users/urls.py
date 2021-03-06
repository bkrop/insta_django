from os import name
from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    register,
    CustomLoginView,
    ProfileDetailView,
    follow_profile,
    search,
    MessageCreateView,
    messages,
    NotificationListView
)
    

urlpatterns = [
    path('login/', CustomLoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('register/', register, name='register'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/follow/<int:pk>', follow_profile, name='follow_profile'),
    path('results/', search, name='search'),
    path('create_message/<int:profile_pk>/', MessageCreateView.as_view(), name='create_message'),
    path('messages/<int:profile_pk>/', messages, name='messages'),
    path('notifications/', NotificationListView.as_view(), name='notifications')
]