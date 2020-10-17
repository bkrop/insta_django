from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.jpg', null=True, blank=True, upload_to='media')

    def __str__(self) -> str:
        return f'{self.user.username}'

class Follow(models.Model):
    follow_to = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='followers')
    follow_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='following')

class Message(models.Model):
    message_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='inbox')
    message_to = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sent')
    content = models.TextField(max_length=250, null=False, blank=False)
    date_of_create = models.DateTimeField(auto_now_add=True)