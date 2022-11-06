from django.urls import path
from . import views


urlpatterns = [
    path('room/', views.CategoryListAPIView.as_view(), name="category-list"),
    path('investment/', views.InvestmentListAPIView.as_view(),
         name="investment-list"),
    path('invest/', views.InvestmentAPIView.as_view(),
         name="post-investment"),

    path('room/<int:id>', views.CategoryDetailAPIView.as_view(),
         name="category-detail"),
    path('room/all/', views.CategoryAllListAPIView.as_view(), name="all-category"),
]
