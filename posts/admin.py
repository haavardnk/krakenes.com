from django.contrib import admin

from .models import BlogPost, Category, Tag

admin.site.register(BlogPost)
admin.site.register(Category)
admin.site.register(Tag)