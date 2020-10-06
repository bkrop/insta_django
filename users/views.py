from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm

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