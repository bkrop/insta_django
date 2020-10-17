from django.contrib import admin
from .models import Follow, Profile, Message

admin.site.register(Profile)
admin.site.register(Follow)
admin.site.register(Message)
