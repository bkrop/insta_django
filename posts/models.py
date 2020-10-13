from django.db import models
from users.models import Profile

class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    description = models.TextField(max_length=200)
    picture = models.ImageField(upload_to='media')
    date_of_create = models.DateTimeField(auto_now_add=True)

    def description_hashtags(self):
        words = self.description.split(' ')
        new_words = []
        new_word = ''
        for word in words:
            if word[0] == '#':
                new_word = f'<a href="/posts/hashtag/{word[1:]}">{word}</a>'
                new_words.append(new_word)
            else:
                new_words.append(word)
        return ' '.join(new_words)

class Hashtag(models.Model):
    name = models.CharField(max_length=20)
    post = models.ManyToManyField(Post, related_name='hashtag')