from django.contrib.sitemaps import Sitemap
from .models import Album

class AlbumSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'
    protocol = 'https'

    def items(self):
        return Album.objects.all().order_by('id')
    
    def lastmod(self, obj):
        return obj.pub_date
