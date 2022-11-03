from django.shortcuts import render
from authentication.models import User
from .models import InvestmentRoom, Investment, Gallery, Investors
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView
from rest_framework import generics, status, views, permissions
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from authentication.utils import serial_investor
from .permissions import IsOwner
from .models import InvestmentRoom

from .serializers import RoomSerializer, GallerySerializer, InvestmentSerializer, InvestorsSerializer
# Create your views here.


class IsSuperUser(IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class CategoryListAPIView(ListCreateAPIView):
    serializer_class = RoomSerializer
    queryset = InvestmentRoom.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser,)

    def perform_create(self, serializer):
        return serializer.save(created_by=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)


class CategoryAllListAPIView(ListAPIView):
    serializer_class = RoomSerializer
    queryset = InvestmentRoom.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.all()


class CategoryDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = RoomSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner,)
    queryset = InvestmentRoom.objects.all()
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.all()
