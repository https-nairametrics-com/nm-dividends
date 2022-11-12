from django.shortcuts import render
from authentication.models import User
from investment.views import IsSuperUser
from investment.models import Investors
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView
from rest_framework import generics, status, views, permissions, filters
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from authentication.utils import serial_investor
from .models import Risk, Interest, InvestmentSize, Period, Expectations

from .serializers import PeriodSerializer, SizeSerializer, RiskSerializer, InterestSerializer, ExpectationsSerializer
from .permissions import IsOwner
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.


class PeriodListAPIView(ListCreateAPIView):
    serializer_class = PeriodSerializer
    queryset = Period.objects.all()
    permission_classes = (IsAuthenticated, IsSuperUser,)
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['period', 'is_verified']
    search_fields = ['period']
    ordering_fields = ['period', 'id', 'is_verified']

    def perform_create(self, serializer):
        return serializer.save(created_by=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)


class PeriodAllListAPIView(ListAPIView):
    serializer_class = PeriodSerializer
    queryset = Period.objects.all()
    #permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['period', 'is_verified']
    search_fields = ['period']
    ordering_fields = ['period', 'id', 'is_verified']

    def get_queryset(self):
        return self.queryset.all()


class PeriodDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = PeriodSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdminUser,)
    queryset = Period.objects.all()
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.all()


class RiskListAPIView(ListCreateAPIView):
    serializer_class = RiskSerializer
    queryset = Risk.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser,)

    def perform_create(self, serializer):
        return serializer.save(created_by=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)


class RiskAllListAPIView(ListAPIView):
    serializer_class = RiskSerializer
    queryset = Risk.objects.all()
    #permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.all()


class RiskDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = RiskSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdminUser,)
    queryset = Risk.objects.all()
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.all()


class InterestListAPIView(ListCreateAPIView):
    serializer_class = InterestSerializer
    queryset = Interest.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser,)

    def perform_create(self, serializer):
        return serializer.save(created_by=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)


class InterestAllListAPIView(ListAPIView):
    serializer_class = InterestSerializer
    queryset = Interest.objects.all()
    #permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.all()


class InterestDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = InterestSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdminUser,)
    queryset = Interest.objects.all()
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.all()


class SizeListAPIView(ListCreateAPIView):
    serializer_class = SizeSerializer
    queryset = InvestmentSize.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser,)

    def perform_create(self, serializer):
        return serializer.save(created_by=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)


class SizeAllListAPIView(ListAPIView):
    serializer_class = SizeSerializer
    queryset = InvestmentSize.objects.all()

    def get_queryset(self):
        return self.queryset.all()


class SizeDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = SizeSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdminUser,)
    queryset = InvestmentSize.objects.all()
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.all()
