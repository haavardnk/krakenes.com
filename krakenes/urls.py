
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from blog import views as blog
from portfolio.views import about, home, album
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from portfolio.sitemaps import AlbumSitemap
from .sitemaps import StaticViewSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'albums': AlbumSitemap
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('search/', blog.search, name='search'),
    path('about/', about, name='about'),
    path('portfolio/', include('portfolio.urls')),
    path('<str:album_slug>/', album, name='album'),
    path('accounts/', include('accounts.urls')),

    path('blog/', include('blog.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^accounts/', include('allauth.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
