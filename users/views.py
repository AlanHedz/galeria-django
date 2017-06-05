# -*- coding: utf-8 -*-:
from __future__ import unicode_literals
from models import User
from images.models import Images

from django.views.generic import View

from forms import LoginUserForm
from forms import RegisterUserForm

from django.contrib.auth import authenticate
from django.contrib.auth import logout as logout_django
from django.contrib.auth import login as login_django

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect

class LoginClass(View):
    template = 'users/login.html'
    form = LoginUserForm()
    message = None

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('index')
        return render(request, self.template, self.get_context())

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user is not None:
            if user.is_activate:
                login_django(request, user)
                return redirect('index')
        return render(request, self.template, self.get_context())

    def get_context(self):
        return {'form': self.form}

class RegisterClass(View):
    template = 'users/register.html'
    form = RegisterUserForm()

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('index')
        return render(request, self.template, self.get_context())

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user_create = User.objects.create_user(username = username,
                                               email = email,
                                               password = password)
        user = authenticate(username = username, password = password)
        if user is not None:
            if user.is_active:
                login_django(request, user)
                return redirect('home')
        return render(request, self.template, self.get_context())

    def get_context(self):
        return {'form': self.form}

def logout(request):
    logout_django(request)
    return redirect('user:login')

class MyImages(LoginRequiredMixin, View):
    login_url = 'user:login'
    template = 'users/my_images.html'

    def get(self, request, *args, **kwargs):
        images = Images.objects.all().filter(user = request.user)
        total_images = images.count()
        return render(request, self.template, {'images': images, 'total_images': total_images})


