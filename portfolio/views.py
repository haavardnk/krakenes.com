from django.shortcuts import render, get_object_or_404, redirect
from posts.models import BlogPost, Comment, Tag, Category
from .models import Photo
from django.core.paginator import Paginator
from django.contrib.postgres.search import SearchVector
from django.db.models import Count
from django.contrib.auth.models import User

def home(request):
    categories = Category.objects.all()
    photos = Photo.objects.all().filter(front_page=True)
    photo_num = list(range(len(photos)))
    return render(request, 'portfolio/home.html', {'photos': photos, 'photo_num': photo_num, 'categories': categories})

def portfolio(request):
    photos = Photo.objects.all().order_by('-id')
    categories = Category.objects.all()
    return render(request, 'portfolio/portfolio.html', {'photos': photos, 'categories': categories})
