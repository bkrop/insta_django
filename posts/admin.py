from django.contrib import admin
from .models import Post, Hashtag, Comment

admin.site.register(Post)
admin.site.register(Hashtag)
admin.site.register(Comment)
