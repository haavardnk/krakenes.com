from django.db import models
from django.contrib.auth.models import User
from posts.models import Category, Tag
from hitcount.models import HitCount
from hitcount.views import HitCountMixin
from ckeditor_uploader.fields import RichTextUploadingField


class Project(models.Model, HitCountMixin, RichTextUploadingField):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    tags = models.ManyToManyField(Tag)
    pub_date = models.DateTimeField()
    content = RichTextUploadingField()
    summary = models.TextField(max_length=150)
    image = models.ImageField(upload_to='images/')
    search_fields = ['title', 'category']

    def __str__(self):
        return self.title

    def pub_date_pretty(self):
        return self.pub_date.strftime('%e %b | %Y')
