from django.shortcuts import render, redirect
from .forms import UserRegisterForm, CustomAuthenticationForm
from django.contrib.auth.views import LoginView
from django.views.generic import DetailView, CreateView
from .models import Profile, Follow, Message
from posts.models import Post
import json
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models import Q

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    context = {'form': form}
    return render(request, 'users/register.html', context)

class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm

class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(author=self.get_object())
        context['following'] = self.request.user.profile.following.values_list('follow_to', flat=True)
        return context

def follow_profile(request, pk):
    profile = Profile.objects.get(pk=pk)
    current_user_profile = request.user.profile
    text = ''
    if Follow.objects.filter(follow_to=profile, follow_by=current_user_profile).exists():
        Follow.objects.get(follow_to=profile, follow_by=current_user_profile).delete()
        print('unfollowed')
        text = 'Follow'
    else:
        Follow.objects.create(follow_to=profile, follow_by=current_user_profile)
        print('followed')
        text = 'Unfollow'
    data = {
        'text': text
    }
    return HttpResponse(json.dumps(data))

def search(request):
    profiles = User.objects.filter(username__contains=request.GET.get('search'))
    context = {
        'profiles': profiles
    }
    return render(request, 'users/results.html', context=context)

class Chat(CreateView):
    model = Message
    fields = ['content']
    template_name = 'users/chat.html'

    def form_valid(self, form):
        form.instance.message_by = self.request.user.profile
        message_to = Profile.objects.get(id=self.kwargs['profile_pk'])
        form.instance.message_to = message_to
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(Chat, self).get_context_data(**kwargs)
        current_user_profile = self.request.user.profile
        second_profile = Profile.objects.get(pk=self.kwargs.get('profile_pk'))
        context['messages'] = Message.objects.filter(
            Q(message_to=current_user_profile, message_by=second_profile)|
            Q(message_to=second_profile, message_by=current_user_profile)).order_by('date_of_create')
        return context