from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from .models import Post, Hashtag, Comment
from users.models import Follow, Notification
import json
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.mixins import UserPassesTestMixin
from .forms import CommentForm
from django.forms.models import model_to_dict
from django.views.generic.edit import FormMixin

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

# class PostListView(FormMixin, ListView):
#     model = Post
#     template_name = 'posts/homepage.html'
#     form_class = CommentForm

#     def get_queryset(self):
#         profiles = Follow.objects.filter(follow_by=self.request.user.profile).values_list('follow_to', flat=True)
#         posts = Post.objects.filter(author_id__in=profiles).order_by('-date_of_create')
#         return posts

#     def post(self, request, *args, **kwargs):
#         form = self.get_form()
#         if form.is_valid():
#             if request.method == 'POST':
#                 pk = self.request.POST.get('pk')
#                 post = Post.objects.get(pk=pk)
#                 new_comment = Comment.objects.create(
#                     author = self.request.user.profile,
#                     post = post,
#                     content = form.cleaned_data['content']
#                 )
#                 return JsonResponse({'comment': model_to_dict(new_comment)}, status=200)
#         else:
#             return self.form_invalid(form)

def homepage(request):
    profiles = Follow.objects.filter(follow_by=request.user.profile).values_list('follow_to', flat=True)
    posts = Post.objects.filter(author_id__in=profiles).order_by('-date_of_create')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            pk = request.POST.get('pk')
            post = Post.objects.get(pk=pk)
            new_comment = Comment.objects.create(
                author = request.user.profile,
                post = post,
                content = form.cleaned_data['content']
            )
            return JsonResponse({'comment': model_to_dict(new_comment)}, status=200)
    form = CommentForm()
    context = {
        'posts': posts,
        'form': form
    }
    return render(request, 'posts/homepage.html', context=context)

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
        'post': post,
    }
    return render(request, 'posts/comments.html', context=context)