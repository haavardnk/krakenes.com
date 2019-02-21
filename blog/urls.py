
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.blog, name='blog'),
    path('<int:post_id>/', views.post, name='post'),
]