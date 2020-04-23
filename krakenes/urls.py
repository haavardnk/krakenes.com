
from django.contrib import admin
from django.urls import path, include
from blog import views as blog
from portfolio import views as portfolio
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', portfolio.home, name='home'),
    path('about/', portfolio.about, name='about'),
    path('accounts/', include('accounts.urls')),
    path('blog/', include('blog.urls')),
    path('portfolio/', include('portfolio.urls')),
    path('search/', blog.search, name='search'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^accounts/', include('allauth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
