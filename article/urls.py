from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.blog_list, name='blog_list'),
    path('posts/create/', views.blog_create, name='blog_create'),
    path('posts/<slug:slug>/', views.blog_detail, name='blog_detail'),  # Use slug instead of id
    path('posts/<slug:slug>/update/', views.blog_update, name='blog_update'),
    path('posts/<slug:slug>/delete/', views.blog_delete, name='blog_delete'),
]
