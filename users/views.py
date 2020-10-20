from django.shortcuts import render, redirect
from .forms import UserRegisterForm, CustomAuthenticationForm
from django.contrib.auth.views import LoginView
from django.views.generic import DetailView, CreateView, ListView
from .models import Profile, Follow, Message, Notification
from posts.models import Post
import json
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.db.models import Q
from django.forms.models import model_to_dict

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

class MessageCreateView(CreateView):
    model = Message
    fields = ['content']
    template_name = 'users/create_message.html'
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            if request.method == 'POST':
                sender = self.request.user.profile
                receiver_pk = self.kwargs['profile_pk']
                print(receiver_pk)
                receiver = Profile.objects.get(id=receiver_pk)
                new_message = Message.objects.create(
                    message_by=sender,
                    message_to=receiver,
                    content = form.cleaned_data['content'])
                return JsonResponse({'message': model_to_dict(new_message)}, status=200)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(MessageCreateView, self).get_context_data(**kwargs)
        profile_pk = context['profile_pk'] = self.kwargs['profile_pk']
        current_user_profile = self.request.user.profile
        second_profile = Profile.objects.get(pk=profile_pk)
        messages = Message.objects.filter(
            Q(message_to=current_user_profile, message_by=second_profile)|
            Q(message_to=second_profile, message_by=current_user_profile)).order_by('date_of_create')
        context['messages'] = messages
        return context

def messages(request, profile_pk):
    current_user_profile = request.user.profile
    second_profile = Profile.objects.get(pk=profile_pk)
    messages = Message.objects.filter(
        Q(message_to=current_user_profile, message_by=second_profile)|
        Q(message_to=second_profile, message_by=current_user_profile)).order_by('date_of_create')
    context = {
        'messages': messages
    }
    return render(request, 'users/messages.html', context=context)

class NotificationListView(ListView):
    model = Notification
    template_name = 'users/notifications.html'

    def get_queryset(self):
        notifications = Notification.objects.filter(profile=self.request.user.profile).all()
        print(notifications)
        notifications.update(is_read=True)
        return notifications