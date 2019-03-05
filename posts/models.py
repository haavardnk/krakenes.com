from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from hitcount.models import HitCount
from hitcount.views import HitCountMixin
from ckeditor_uploader.fields import RichTextUploadingField


class Category(models.Model):
    name = models.CharField(max_length=32)

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


class BlogPost(models.Model, HitCountMixin, RichTextUploadingField):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    tags = models.ManyToManyField(Tag)
    pub_date = models.DateTimeField(default=timezone.now)
    content = RichTextUploadingField()
    summary = models.TextField(max_length=150)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

    def comment_count(self):
        return self.comments.filter(approved_comment=True).count()

    def pub_date_pretty(self):
        return self.pub_date.strftime('%e %b | %Y')

class Comment(models.Model):
    post = models.ForeignKey(
        BlogPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def __str__(self):
        return self.text
