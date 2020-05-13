from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFit
from exiffield.fields import ExifField
from exiffield.getters import exifgetter
from django.utils.text import slugify

class Album(models.Model):
    title = models.CharField(max_length=50)
    sub_title = models.CharField(max_length=75, blank=True)
    image = models.ImageField(upload_to='images/albums')
    image_small = ImageSpecField(source='image',
                                      processors=[ResizeToFit(width=1024, upscale=False)],
                                      format='JPEG',
                                      options={'quality': 80})
    slug = models.SlugField(unique=True, default='will-auto-update')
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Album, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Albums"

    def __str__(self):
        return self.title

class Photo(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=150, blank=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, blank=True, null=True)
    pub_date = models.DateTimeField(default=timezone.now)
    photo_full = models.ImageField(upload_to='photos')
    photo_thumb = ImageSpecField(source='photo_full',
                                      processors=[ResizeToFit(width=400, upscale=False)],
                                      format='JPEG',
                                      options={'quality': 80})
    photo_large = ImageSpecField(source='photo_full',
                                      processors=[ResizeToFit(width=2048, upscale=False)],
                                      format='JPEG',
                                      options={'quality': 80})
    portfolio = models.BooleanField(default=False)
    exif = ExifField(
        source='photo_full',
    )

    class Meta:
        verbose_name_plural = "Photos"

    def __str__(self):
        return self.title

class Frontpage(models.Model):
    image = models.ForeignKey(Photo, on_delete=models.CASCADE)
    order = models.IntegerField(blank=False)

class Site(models.Model):
    site_name = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    sub_title = models.CharField(max_length=75, blank=True)
    background = models.ImageField(upload_to='images/sites')
    background_small = ImageSpecField(source='background',
                                      processors=[ResizeToFit(width=1024, upscale=False)],
                                      format='JPEG',
                                      options={'quality': 80})

    def __str__(self):
        return self.site_name