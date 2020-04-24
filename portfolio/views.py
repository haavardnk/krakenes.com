from django.shortcuts import render, get_object_or_404, redirect
from posts.models import BlogPost, Comment, Tag, Category
from .models import Photo, Site
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
    site_settings = get_object_or_404(Site, site_name="portfolio")
    photos = Photo.objects.all().order_by('id')
    categories = Category.objects.all()
    exif_list = []
    for photo in photos:
        exif_list.append({
            'filename' : photo.exif['FileName']['val'],
            'date' : photo.exif['DateTimeOriginal']['val'],
            'aperture' : photo.exif['Aperture']['val'],
            'exposure' : photo.exif['ExposureTime']['val'],
            'iso' : photo.exif['ISO']['val'],
            'focallength' : photo.exif['FocalLength']['val'],
            'lens' : photo.exif['LensModel']['val'],
            'model' : photo.exif['Model']['val'],
            'make' : photo.exif['Make']['val'],
        })
    photos_exif = zip(photos, exif_list)
    print(photos[0].exif['Model']['val'])
    return render(request, 'portfolio/portfolio.html', {'photos_exif': photos_exif, 'categories': categories, 'site_settings': site_settings})

def about(request):
    site_settings = get_object_or_404(Site, site_name="about")
    categories = Category.objects.all()
    return render(request, 'portfolio/about.html', {'categories': categories, 'site_settings': site_settings})
