from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.shortcuts import redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404



class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'blog/register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, 'blog/register.html', {'form': form})


@login_required
def profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        bio = request.POST.get('bio', profile.bio)
        profile.bio = bio
        profile.save()
        return redirect('profile')
    return render(request, 'blog/edit_profile.html', {'profile': profile})


def home(request):
    return render(request, 'blog/home.html')	



