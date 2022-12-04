from django.urls import path
from . import views


urlpatterns = [
    path('admin/list/', views.AdminGroupCommentListAPIView.as_view(),
         name="comment-list"),
    path('create/<int:id>', views.CreateCommentAPIView.as_view(),
         name="create-comment"),
    path('admin/create/<int:id>', views.AdminCreateCommentAPIView.as_view(),
         name="admin-create-comment"),
    path('investor/<int:id>', views.InvestorDetailAPIView.as_view(),
         name="investor-comment"),
]
