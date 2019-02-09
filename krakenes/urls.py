
from django.contrib import admin
from django.urls import path, include
from blog import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('accounts/', include('accounts.urls')),
    path('blog/', include('blog.urls')),
    path('projects/', include('projects.urls')),
    path('avatar/', include('avatar.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)