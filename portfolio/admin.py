from django.contrib import admin

# Register your models here.
from .models import Photo, Site, Album, Frontpage

admin.site.register(Photo)
admin.site.register(Album)
admin.site.register(Site)
admin.site.register(Frontpage)