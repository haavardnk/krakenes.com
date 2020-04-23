from django.contrib import admin

# Register your models here.
from .models import Photo, Site

admin.site.register(Photo)
admin.site.register(Site)