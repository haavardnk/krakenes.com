from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField


class Category(models.Model):
    name = models.CharField(max_length=32)
    image = models.ImageField(upload_to='images/categories', blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class BlogPost(models.Model, RichTextUploadingField):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=50, blank=True)
    content = RichTextUploadingField()
    summary = models.TextField(max_length=150)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

    def comment_count(self):
        return self.comments.filter(approved_comment=True).count()

    def pub_date_pretty(self):
        return self.pub_date.strftime('%e %b %Y')

class Comment(models.Model):
    post = models.ForeignKey(
        BlogPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=True)

    def __str__(self):
        return self.text
