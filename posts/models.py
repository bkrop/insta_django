from django.db import models
from users.models import Profile

class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    description = models.TextField(max_length=200)
    picture = models.ImageField(upload_to='media')
    date_of_create = models.DateTimeField(auto_now_add=True)
