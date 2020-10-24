from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from .models import Post, Hashtag, Comment
from users.models import Follow, Notification
import json
from django.http import HttpResponse
from django.contrib.auth.mixins import UserPassesTestMixin

class PostCreateView(CreateView):
    model = Post
    template_name = 'posts/create_post.html'
    fields = ['picture', 'description']

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        self.object = form.save()
        words = form.cleaned_data['description'].split(" ")
        for word in words:
                if word[0] == "#":
                    hashtag, created = Hashtag.objects.get_or_create(name=word[1:])
                    hashtag.post.add(self.object)
        return super().form_valid(form)

class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/detail_post.html'

class PostListView(ListView):
    model = Post
    template_name = 'posts/homepage.html'

    def get_queryset(self):
        profiles = Follow.objects.filter(follow_by=self.request.user.profile).values_list('follow_to', flat=True)
        posts = Post.objects.filter(author_id__in=profiles).order_by('-date_of_create')
        return posts

class PostUpdateView(UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'posts/create_post.html'
    fields = ['picture', 'description']

    def test_func(self):
        post = self.get_object()
        if self.request.user.profile == post.author:
            return True
        else:
            return False

def hashtag_posts(request, hashtag):
    hashtag = Hashtag.objects.get(name=hashtag)
    object_list = hashtag.post.all().order_by('-date_of_create')
    print(object_list)
    context = {
        'object_list': object_list
    }
    return render(request, 'posts/homepage.html', context=context)
        
def like_post(request, post_id):
    post = Post.objects.get(id=post_id)
    profile = request.user.profile
    like = None
    if profile in post.like.all():
        post.like.remove(profile)
        like = False
    else:
        post.like.add(profile)
        like = True
        Notification.objects.create(profile=post.author, message=f'{profile} liked your {post}')
    data = {
        'counter': post.likes_counter(),
        'like': like
    }
    return HttpResponse(json.dumps(data))

def post_comments(request, pk):
    post = Post.objects.get(pk=pk)
    context = {
        'post': post
    }
    return render(request, 'posts/comments.html', context=context)