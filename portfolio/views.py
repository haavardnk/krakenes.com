from django.shortcuts import render, get_object_or_404, redirect
from .models import Photo, Site, Album, Frontpage, Portfolio
from django.core.paginator import Paginator
from django.contrib.postgres.search import SearchVector
from django.db.models import Count
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from meta.views import Meta
from django.urls import reverse

def home(request):
    site_settings = get_object_or_404(Site, site_name="home")
    frontpage_elements = Frontpage.objects.all().order_by('order')
    photo_num = list(range(len(frontpage_elements)))
    meta = Meta(
        use_title_tag=True,
        title=site_settings.meta_title,
        description=site_settings.meta_description,
        url=reverse('home'),
        image=frontpage_elements[0].image.photo_thumb.url,
        keywords=['photography', 'portfolio', 'cars', 'automotive', 'automotive photography', 'porsche', 'car photography', 'krakenes photography', 'kråkenes photography', 'håvard kråkenes'],
        object_type='website',
        use_facebook=True
        )
    return render(request, 'portfolio/home.html', {'site_settings': site_settings, 'frontpage_elements': frontpage_elements, 'photo_num': photo_num, 'meta': meta})

def portfolio(request):
    site_settings = get_object_or_404(Site, site_name="portfolio")
    photos = Portfolio.objects.all().order_by('order')
    meta = Meta(
        use_title_tag=True,
        title=site_settings.meta_title,
        description=site_settings.meta_description,
        url=reverse('portfolio'),
        image=site_settings.background_small.url,
        object_type='website',
        use_facebook=True
        )
    exif_list = []
    photo_list = []
    for photo in photos:
        exif_list.append({
            'filename' : photo.image.exif['FileName']['val'],
            'date' : photo.image.exif['DateTimeOriginal']['val'],
            'aperture' : photo.image.exif['Aperture']['val'],
            'exposure' : photo.image.exif['ExposureTime']['val'],
            'iso' : photo.image.exif['ISO']['val'],
            'focallength' : photo.image.exif['FocalLength']['val'],
            'lens' : photo.image.exif['LensModel']['val'],
            'model' : photo.image.exif['Model']['val'],
            'make' : photo.image.exif['Make']['val'],
        })
        photo_list.append(photo.image)

    photos_exif = zip(photo_list, exif_list)
    return render(request, 'portfolio/gallery.html', {'photos_exif': photos_exif, 'site_settings': site_settings, 'meta': meta})

def album(request, album_slug):
    if request.method == 'POST' and 'title' in request.POST:
        title = request.POST.get('title')
        image = request.FILES.get('image')
        
        album = Album.objects.create(title=title, image=image)
        album.save()

        return redirect('album', album_slug=album.slug)

    elif request.method == 'POST' and 'slug' in request.POST:
        slug = request.POST.get('slug')
        album = get_object_or_404(Album, slug=slug)
        for i in request.FILES.getlist('images'):
            Photo.objects.create(album=album, photo_full=i)
        return redirect('album', album_slug=album.slug)

    album = get_object_or_404(Album, slug=album_slug)
    photos = Photo.objects.all().filter(album=album).order_by('order')
    exif_list = []
    site_settings = {'title' : album.title,'sub_title' : album.sub_title,'background_small' : album.image_small}
    meta = Meta(
        use_title_tag=True,
        title=album.title+" - Kråkenes Photography",
        description=album.sub_title,
        url=album.get_absolute_url(),
        image=album.image_small.url,
        object_type='website',
        use_facebook=True
        )

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
    return render(request, 'portfolio/gallery.html', {'photos_exif': photos_exif, 'site_settings': site_settings, 'meta': meta, 'slug': album.slug})

def about(request):
    site_settings = get_object_or_404(Site, site_name="about")
    meta = Meta(
        use_title_tag=True,
        title=site_settings.meta_title,
        description=site_settings.meta_description,
        url=reverse('about'),
        image=site_settings.background_small.url,
        object_type='website',
        use_facebook=True
        )
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

    return render(request, 'portfolio/about.html', {'site_settings': site_settings, 'meta': meta})
