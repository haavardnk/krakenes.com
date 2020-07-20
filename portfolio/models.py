from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFit, ResizeToFill
from exiffield.fields import ExifField
from exiffield.getters import exifgetter
from django.utils.text import slugify
from django.urls import reverse

class Album(models.Model):
    title = models.CharField(max_length=50)
    sub_title = models.CharField(max_length=75, blank=True)
    pub_date = models.DateTimeField(default=timezone.now)
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

    def get_absolute_url(self):
        return reverse('album', args=[str(self.slug)])

class Photo(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0, blank=False, null=False)
    pub_date = models.DateTimeField(default=timezone.now)
    photo_full = models.ImageField(upload_to='photos')
    photo_thumb = ImageSpecField(source='photo_full',
                                      processors=[ResizeToFill(width=400, height=267, upscale=False)],
                                      format='JPEG',
                                      options={'quality': 80})
    photo_mini_thumb = ImageSpecField(source='photo_full',
                                      processors=[ResizeToFit(width=200, upscale=False)],
                                      format='JPEG',
                                      options={'quality': 80})
    photo_large = ImageSpecField(source='photo_full',
                                      processors=[ResizeToFit(width=2048, upscale=False)],
                                      format='JPEG',
                                      options={'quality': 80})
    portfolio_bool = models.BooleanField(default=False)
    frontpage_bool = models.BooleanField(default=False)
    exif = ExifField(
        source='photo_full',
    )

    class Meta:
        verbose_name_plural = "Photos"
        ordering = ['order']

    def __str__(self):
        return self.photo_full.name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.portfolio_bool and not Portfolio.objects.filter(image=self):
            Portfolio.objects.create(image=self)
        elif Portfolio.objects.filter(image=self) and not self.portfolio_bool:
            Portfolio.objects.filter(image=self).delete()

        if self.frontpage_bool and not Frontpage.objects.filter(image=self):
            Frontpage.objects.create(image=self)
        elif Frontpage.objects.filter(image=self) and not self.frontpage_bool:
            Frontpage.objects.filter(image=self).delete()

class Frontpage(models.Model):
    image = models.OneToOneField(Photo, on_delete=models.CASCADE, unique=True)
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

class Portfolio(models.Model):
    image = models.OneToOneField(Photo, on_delete=models.CASCADE, unique=True)
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

class Site(models.Model):
    site_name = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    sub_title = models.CharField(max_length=75, blank=True)
    background = models.ImageField(upload_to='images/sites', null=True, blank=True)
    background_small = ImageSpecField(source='background',
                                      processors=[ResizeToFit(width=1440, upscale=False)],
                                      format='JPEG',
                                      options={'quality': 80})
    text1 = models.TextField(max_length=500, blank=True)
    text2 = models.TextField(max_length=500, blank=True)
    photo1 = models.ImageField(upload_to='images/sites', null=True, blank=True)
    photo1_thumb = ImageSpecField(source='photo1',
                                      processors=[ResizeToFit(width=200, upscale=False)],
                                      format='JPEG',
                                      options={'quality': 80})
    meta_title = models.CharField(max_length=100, blank=True)
    meta_description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.site_name