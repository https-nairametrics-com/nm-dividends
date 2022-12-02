from django.urls import path
from . import views


urlpatterns = [
    path('admin/list/', views.AdminUserCommentListAPIView.as_view(),
         name="comment-list"),
    path('create/<int:id>', views.CreateCommentAPIView.as_view(),
         name="create-comment"),
    path('admin/create/<int:id>', views.AdminCreateCommentAPIView.as_view(),
         name="admin-create-comment"),
]
