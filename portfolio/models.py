from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit

class Photo(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
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
    front_page = models.BooleanField(default=False)


    class Meta:
        verbose_name_plural = "Photos"

    def __str__(self):
        return self.title