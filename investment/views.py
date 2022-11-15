from django.shortcuts import render
from authentication.models import User
from .models import InvestmentRoom, Investment, Gallery, Investors
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView
from rest_framework import generics, status, views, permissions
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from authentication.utils import serial_investor
from .permissions import IsOwner, IsInvestmentOwner
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .serializers import TotalInvestmentSerializer, InvestmentOnlySerializer, RoomSerializer, GallerySerializer, InvestmentSerializer, InvestorsSerializer
from investor.serializers import RiskSerializer
from investor.models import Risk, Period, InvestmentSize, Interest
from django.db.models import Sum, Aggregate, Avg
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
    #permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.all()


class CategoryDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = RoomSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdminUser,)
    queryset = InvestmentRoom.objects.all()
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.all()


class InvestmentListAPIView(ListAPIView):
    serializer_class = InvestmentSerializer
    queryset = Investment.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser,)
    #parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class InvestmentAPIView(generics.GenericAPIView):
    serializer_class = InvestmentOnlySerializer
    gallery_serializer = GallerySerializer
    permission_classes = (IsAuthenticated, IsAdminUser,)
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        indata = {
            # 'owner': self.request.user,
            'name': request.data.get('name'),
            'description': request.data.get('description'),
            'room': request.data.get('room'),
            'period': request.data.get('period'),
            'roi': request.data.get('roi'),
            'annualized': request.data.get('annualized'),
            'risk': request.data.get('risk'),
            'amount': request.data.get('amount'),
            'features': request.data.get('features'),
            'is_verified': request.data.get('is_verified'),
        }
        serializer = self.serializer_class(data=indata)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=self.request.user)
        investment_data = serializer.data
        imagedata = {'investment': investment_data['id'],
                     'gallery': request.data.get('gallery'),
                     'is_featured': request.data.get('is_featured')}
        in_serializer = self.gallery_serializer(data=imagedata)
        in_serializer.is_valid(raise_exception=True)
        in_serializer.save()
        return Response(indata, status=status.HTTP_201_CREATED)


class TotalInvesmentAmountAPIView(generics.GenericAPIView):
    serializer_class = TotalInvestmentSerializer
    #permission_classes = (IsAuthenticated)

    def get(self, format=None):
        try:
            queryset = Investment.objects.aggregate(amount=Sum('amount'))
            serializer = TotalInvestmentSerializer(queryset, many=True)
            print(serializer.data)
            return Response(serializer.data)
        except:
            return Response(
                {'error': 'Something went wrong when trying to load user'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
