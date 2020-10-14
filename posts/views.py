from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView
from .models import Post, Hashtag
from users.models import Follow

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
    if profile in post.like.all():
        post.like.remove(profile)
    else:
        post.like.add(profile)