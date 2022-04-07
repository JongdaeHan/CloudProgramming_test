import os.path

from django.contrib.auth.models import User
from django.core.management.commands.makemessages import plural_forms_re
from django.db import models


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural : 'Categories'

    def get_absolute_url(self):
        return f'/blog/category/{self.slug}/'


class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE )
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 모델 메소드 정의(오버라이드)
    def __str__(self):
        return f'[{self.pk}]   [{self.title}] :: {self.author}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)


