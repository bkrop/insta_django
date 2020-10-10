from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView
from .models import Post
from users.models import Follow

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

class PostListView(ListView):
    model = Post
    template_name = 'posts/homepage.html'

    def get_queryset(self):
        profiles = Follow.objects.filter(follow_by=self.request.user.profile).values_list('follow_to', flat=True)
        posts = Post.objects.filter(author_id__in=profiles)
        print(profiles)
        print(posts)
        return posts