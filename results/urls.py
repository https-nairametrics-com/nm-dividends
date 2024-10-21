from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_csv, name='upload_csv'),
    path('my-uploads/', views.user_uploads, name='user_uploads'),  # View user's uploads
    path('uploads/', views.view_all_uploads, name='view_upload_csv'),
    path('nmdata/<int:pk>/update/', views.upload_csv, name='update_upload'),
]