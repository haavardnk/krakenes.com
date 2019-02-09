from django.contrib import admin

from .models import BlogPost, Category, Tag, Comment

admin.site.register(BlogPost)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Tag)