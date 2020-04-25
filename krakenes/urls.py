
from django.contrib import admin
from django.urls import path, include
from blog import views as blog
from portfolio.views import about, home, album
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static

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
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
