from django.contrib import admin
from .models import Follow, Profile, Message, Notification

admin.site.register(Profile)
admin.site.register(Follow)
admin.site.register(Message)
admin.site.register(Notification)
