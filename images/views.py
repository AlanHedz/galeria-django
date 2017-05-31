# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from models import Images
from models import Comments

from forms import CreateImageForm
from forms import CreateCommentForm

from django.views.generic import CreateView
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin

from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy, reverse

def index(request):
    images = Images.objects.all()
    return render(request, 'index.html', {'images': images})

class CreateClass(LoginRequiredMixin, CreateView):
    login_url = 'user:login'
    model = Images
    form_class = CreateImageForm
    template_name = 'images/create.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('images:show', kwargs={'slug': self.object.slug})

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(CreateClass, self).get_form_kwargs(*args, **kwargs)
        return kwargs

class ShowClass(SingleObjectMixin, View):
    model = Images
    template_name = 'images/show.html'
    slug_field = 'slug'

    def get(self, request, *args, **kwargs):
        form = CreateCommentForm()
        comments = Comments.objects.all().filter(image = self.get_object())
        return render(request, self.template_name, {'image': self.get_object(), 'form': form, 'comments': comments})