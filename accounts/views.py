from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import UserRegistrationForm, UserLoginFrom, ProfileImageForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile
from rest_framework.permissions import IsAuthenticated


class UserRegister(View):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(username=cd['username'], email=cd['email'], password=cd['password'])
            Profile.objects.create(user=user)
            messages.success(request, 'you registered successfully', 'info')
            return redirect('core:home')
        return render(request, self.template_name, {'form': form})


class UserLogin(View):
    form_class = UserLoginFrom
    template_name = 'accounts/login.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'you logged in successfully', 'info')
                return redirect('core:home')
            messages.error(request, 'username or password is wrong', 'warning')
        return render(request, self.template_name, {'form': form})


class UserLogout(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'you logged out successfully', 'info')
        return redirect('core:home')

class UserDashboard(LoginRequiredMixin, View):
    template_name = 'accounts/dashboard.html'
    form_class = ProfileImageForm

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        form = self.form_class
        return render(request, self.template_name, {'user': user, 'form': form})

    def post(self, request, *arks, **kwargs):
        form = self.form_class(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'your image uploaded successfully', 'info')
            return redirect('accounts:dashboard', request.user.username)




