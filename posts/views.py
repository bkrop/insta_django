from django.shortcuts import render
from django.views.generic import CreateView, DetailView
from .models import Post

class PostCreateView(CreateView):
    model = Post
    template_name = 'posts/create_post.html'
    fields = ['picture', 'description']

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)

class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/detail_post.html'
