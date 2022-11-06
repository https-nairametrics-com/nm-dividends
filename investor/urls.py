from django.urls import path
from . import views


urlpatterns = [
    path('period/', views.PeriodListAPIView.as_view(), name="period-list"),
    path('period/<int:id>', views.PeriodDetailAPIView.as_view(),
         name="period-detail"),
    path('period/all/', views.PeriodAllListAPIView.as_view(), name="all-period"),
    path('risk/', views.RiskListAPIView.as_view(), name="risk-list"),
    path('risk/<int:id>', views.RiskDetailAPIView.as_view(),
         name="risk-detail"),
    path('risk/all/', views.RiskAllListAPIView.as_view(), name="all-risk"),
]
