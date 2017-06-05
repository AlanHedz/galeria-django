# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from models import Images
from models import Comments

from forms import CreateImage
from forms import CreateCommentForm

from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect, HttpResponse
from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse_lazy, reverse
import json

def index(request):
	images = Images.objects.all().order_by('created_at')[0:5]
	return render(request, 'index.html', {'images': images})

def create_image(request):
	if request.method == 'POST':
		form = CreateImage(request.POST or None, request.FILES or None)
		if form.is_valid():
			image = request.FILES['imageFile']
			title = request.POST['title']
			i = Images.objects.create(image = image, title = title, user = request.user)
			i.save()
			return redirect('user:my_images')
	else:
		form = CreateImage()
	return render(request, 'images/create.html', {'form': form})

def show_image(request, slug):
	image = Images.objects.get(slug=slug)
	form = CreateCommentForm()
	comments = Comments.objects.all().filter(image = image)
	return render(request, 'images/show.html', {'image': image, 'form': form, 'comments': comments})

def create_comment(request):
	if request.method == 'POST':
		form = CreateCommentForm(request.POST or None)
		if form.is_valid():
			user = request.user
			text = request.POST['text']
			image = request.POST['image']
			Comments.objects.create(image = image, user = user, text = text)
			return redirect(reverser('images:show', kwargs={'slug': image.slug}))
		else:
			return redirect(reverser('images:show', kwargs={'slug': image.slug}))

def edit_image(request, pk):
	image =  Images.objects.get(pk=pk)
	if request.user == image.user:
		if request.method == 'POST':
			form = CreateImage(request.POST or None, request.FILES or None)
			if form.is_valid():
				image.image = request.FILES['imageFile']
				image.title = request.POST['title']
				image.save()
				return redirect('user:my_images')
		else:
			form = CreateImage()
	else:
		redirect('user:my_images')
	return render(request, 'images/edit.html', {'image': image, 'form': form})

@login_required(login_url='user:login')
def delete_image(request, pk):
	image = Images.objects.get(pk=pk)
	if request.method == 'POST':
		if image.user == request.user:
			image.comments_set.all().delete()
			image.delete()
			return redirect('user:my_images')
		else:
			return redirect('index')

@login_required(login_url='user:login')
def like_image(request, slug):
	if request.method == 'POST':
		user = request.user
		slug = request.POST.get('slug')
		image = Images.objects.get(slug = slug)

		if image.likes.filter(id = user.id).exists():
			image.likes.remove(user)
			message = 'No me gusto'
		else:
			image.likes.add(user)
			message = 'Me gusto'
	ctx = {'likes_count': image.total_likes, 'message': message}
	print image.total_likes
	return HttpResponse(json.dumps(ctx), content_type='application/json')