from django.shortcuts import render
from authentication.models import User
from investment.views import IsSuperUser
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView
from rest_framework import generics, status, views, permissions
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from authentication.utils import serial_investor
from .models import Risk, Interest, InvestmentSize, Period, Expectations, Investor
from .serializers import PeriodSerializer, SizeSerializer, RiskSerializer, InterestSerializer, ExpectationsSerializer
from .permissions import IsOwner
# Create your views here.


class PeriodListAPIView(ListCreateAPIView):
    serializer_class = PeriodSerializer
    queryset = Period.objects.all()
    permission_classes = (IsAuthenticated, IsSuperUser,)

    def perform_create(self, serializer):
        return serializer.save(created_by=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)


class PeriodAllListAPIView(ListAPIView):
    serializer_class = PeriodSerializer
    queryset = Period.objects.all()
    #permission_classes = (IsAuthenticated,)

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
    #permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.all()


class SizeDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = SizeSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdminUser,)
    queryset = InvestmentSize.objects.all()
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.all()
