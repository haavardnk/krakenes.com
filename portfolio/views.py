from django.shortcuts import render, get_object_or_404, redirect
from posts.models import BlogPost, Comment, Tag, Category
from .models import Photo, Site, Album
from django.core.paginator import Paginator
from django.contrib.postgres.search import SearchVector
from django.db.models import Count
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse

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
    return render(request, 'portfolio/gallery.html', {'photos_exif': photos_exif, 'categories': categories, 'site_settings': site_settings})

def album(request, album_slug):
    album = get_object_or_404(Album, slug=album_slug)
    photos = Photo.objects.all().filter(album=album).order_by('id').distinct('id')
    categories = Category.objects.all()
    exif_list = []
    site_settings = {'title' : album.title,'sub_title' : album.sub_title,'background' : album.image}

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
    return render(request, 'portfolio/gallery.html', {'photos_exif': photos_exif, 'categories': categories, 'site_settings': site_settings})

def about(request):
    site_settings = get_object_or_404(Site, site_name="about")
    categories = Category.objects.all()

    if request.method == 'POST' and request.is_ajax:
        response_data = {}
        name = request.POST.get('name')
        from_email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        try: 
            send_mail(
            name+' - '+subject+' - '+from_email,
            message,
            'krakenesphotography@gmail.com',
            ['krakenesphotography@gmail.com'],
            fail_silently=False)
            response_data['send'] = "success"
            
        except:
            response_data['send'] = "failed"
        return HttpResponse(JsonResponse(response_data))

    return render(request, 'portfolio/about.html', {'categories': categories, 'site_settings': site_settings})
