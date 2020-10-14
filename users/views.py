from django.shortcuts import render, redirect
from .forms import UserRegisterForm, CustomAuthenticationForm
from django.contrib.auth.views import LoginView
from django.views.generic import DetailView
from .models import Profile, Follow
from posts.models import Post
import json
from django.http import HttpResponse
from django.contrib.auth.models import User

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