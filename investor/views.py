from django.shortcuts import render
from authentication.models import User
from investment.views import IsSuperUser
from investment.models import Investors, Investment
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView
from rest_framework import generics, status, views, permissions, filters
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from authentication.utils import serial_investor, investor_slug
from .models import Risk, Interest, InvestmentSize, Period, Expectations
from .serializers import CreateInvestorSerializer, ApproveInvestorSerializer, CloseInvestorSerializer, InvestorSerializer, AdminInvestorSerializer, PeriodSerializer, SizeSerializer, RiskSerializer, InterestSerializer, ExpectationsSerializer
from .permissions import IsOwner, IsUserApproved
from django.db.models import Sum, Aggregate, Avg
from django.http import JsonResponse, Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
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


class InvestmentAPIView(generics.GenericAPIView):
    serializer_class = CreateInvestorSerializer
    queryset = Investors.objects.all().order_by('-created_at')
    permission_classes = (IsAuthenticated, IsUserApproved,)
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    def get_object(self, id):
        try:
            return Investment.objects.get(id=id)
        except Investment.DoesNotExist:
            raise Http404

    def post(self, request, id, format=None):
        investment_id = self.get_object(id)
        investordata = {
            'amount': request.data.get('amount'),
            'slug': str(investor_slug()),
            'investment': id,
            'investor': request.user.id,
            'serialkey': str(serial_investor()),
            'is_approved': False,
            'is_closed': False,
        }
        serializer = self.serializer_class(data=investordata)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class InvestorListAPIView(ListAPIView):
    serializer_class = InvestorSerializer
    queryset = Investors.objects.all().order_by('-created_at')
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    def get_queryset(self):
        return self.queryset.filter(investor=self.request.user)


class InvestorAdminListAPIView(generics.GenericAPIView):
    serializer_class = InvestorSerializer
    queryset = Investors.objects.all().order_by('-created_at')
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    def get_object(self, pk):
        try:
            return Investors.objects.get(id=pk)
        except Investors.DoesNotExist:
            raise Http404


class ApproveInvestmentAPIView(generics.GenericAPIView):
    serializer_class = ApproveInvestorSerializer
    queryset = Investors.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser,)
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    def get_object(self, pk):
        try:
            return Investment.objects.get(id=pk)
        except Investment.DoesNotExist:
            raise Http404

    def patch(self, request, pk, format=None):
        investment_id = self.get_object(pk)
        investordata = {
            'is_approved': request.data.get('is_closed'),
            'approved_by': self.request.user,
        }
        serializer = self.serializer_class(investment_id, data=investordata)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CloseInvestmentAPIView(generics.GenericAPIView):
    serializer_class = ApproveInvestorSerializer
    queryset = Investors.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser,)
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    def get_object(self, pk):
        try:
            return Investment.objects.get(id=pk)
        except Investment.DoesNotExist:
            raise Http404

    def patch(self, request, pk, format=None):
        investment_id = self.get_object(pk)
        investordata = {
            'is_closed': request.data.get('is_closed'),
            'closed_by': self.request.user,
        }
        serializer = self.serializer_class(investment_id, data=investordata)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
