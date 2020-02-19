from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField


class Category(models.Model):
    name = models.CharField(max_length=32)
    image = models.ImageField(upload_to='images/categories')

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
    tags = models.ManyToManyField(Tag, blank=True)
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, default='will-auto-update')
    content = RichTextUploadingField()
    summary = models.TextField(max_length=255)
    image = models.ImageField(upload_to='images/')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(BlogPost, self).save(*args, **kwargs)

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
