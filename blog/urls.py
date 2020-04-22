
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.blog, name='blog'),
    path('<str:post_slug>/', views.post, name='post'),
    path('category/<str:category_name>/', views.category, name='category'),
]