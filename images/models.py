# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.db import models

class Images(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="images")
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        self.slug = self.title.replace(' ', '-').lower()
        super(Images, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class Comments(models.Model):
    text = models.TextField(max_length=200)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ForeignKey(Images, on_delete=models.CASCADE)

    def __str__(self):
        return text
