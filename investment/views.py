from django.shortcuts import render
from authentication.models import User, Profile
from .models import SponsorInvestment, Sponsor, Currency, DealType, MainRoom, InvestmentRoom, Investment, Gallery, Investors
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView
from rest_framework import filters, generics, status, views, permissions
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from authentication.utils import serial_investor
from authentication.serializers import ProfileSerializer, RegisterSerializer
from .permissions import IsOwner, IsInvestmentOwner
from authentication.utils import Util, serial_investor, username_generator, referral_generator, investor_slug
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .serializers import FileUploadSerializer, InvestmentDetailsSerializer, IssuerInvestorSerializer, IssuerOnlySerializer, UpdateSponsorSerializer, ListSponsorInvestmentSerializer, SponsorListSerializer, ApproveSponsorSerializer, SponsorSerializer, SponsorInvestmentSerializer, CurrencySerializer, DealTypeSerializer, MainRoomSerializer, CreateRoomSerializer, GalleryUpdateSerializer, CloseInvestmentSerializer, GalleryUDSerializer, ApproveInvestmentSerializer, TotalInvestmentSerializer, InvestmentRoomSerializer, InvestmentOnlySerializer, RoomSerializer, GallerySerializer, InvestmentSerializer
from investor.serializers import RiskSerializer, CreateInvestorSerializer
from investor.models import Risk, Period, InvestmentSize, Interest
from django.db.models import Sum, Aggregate, Avg, Count, F
from django.http import JsonResponse, Http404, HttpResponse
import json
import pandas as pd
from itertools import chain
from .helpers import modify_input_for_multiple_files
from decimal import *
from django_filters.rest_framework import DjangoFilterBackend
import csv
from . import serializers
from django.core.mail import send_mail as sender
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
# Create your views here.


def getSponsorId(nin):
    query = Sponsor.objects.filter(
        nin=nin)
    return query


def checkSponsored(id):
    query = SponsorInvestment.objects.filter(investment=id)
    return query


def checkNin(id):
    query = Profile.objects.filter(nin=id)
    return query


def getInvestorId(nin):
    query = Profile.objects.filter(nin=nin)
    if query:
        getId = Profile.objects.filter(
            nin=nin).values_list('user', flat=True)[0]

    return int(getId)


def checkInvestorExist(nin, id):
    query2 = Investors.objects.filter(
        investment=id, investor=getInvestorId(nin))
    return query2


def checkInvestorInvestment(invt, id):
    query = Investors.objects.filter(investment=invt, id=id)
    return query


def checkInvestmentOwner(user, id):
    query = Investment.objects.filter(owner=user, id=id)
    return query


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        # 👇️ if passed in object is instance of Decimal
        # convert it to a string
        if isinstance(obj, Decimal):
            return str(obj)
        # 👇️ otherwise use the default behavior
        return json.JSONEncoder.default(self, obj)


class IsSuperUser(IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class MainRoomListAPIView(ListCreateAPIView):
    serializer_class = MainRoomSerializer
    queryset = MainRoom.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser,)

    def perform_create(self, serializer):
        return serializer.save(created_by=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)


class MainRoomAllListAPIView(ListAPIView):
    serializer_class = MainRoomSerializer
    queryset = MainRoom.objects.all()
    # permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.all()


class CurrencyListAPIView(ListAPIView):
    serializer_class = CurrencySerializer
    queryset = Currency.objects.all()
    # permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.all()


class CurrencyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CurrencySerializer
    permission_classes = (permissions.IsAuthenticated, IsAdminUser,)
    queryset = Currency.objects.all()
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.all()


class CurrencyAListAPIView(ListCreateAPIView):
    serializer_class = CurrencySerializer
    queryset = Currency.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser,)

    def perform_create(self, serializer):
        return serializer.save()

    def get_queryset(self):
        return self.queryset.all()


class DealTypeListAPIView(ListAPIView):
    serializer_class = DealTypeSerializer
    queryset = DealType.objects.all()
    # permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.all()


class DealTypeAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = DealTypeSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdminUser,)
    queryset = DealType.objects.all()
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.all()


class DealTypeAListAPIView(ListCreateAPIView):
    serializer_class = DealTypeSerializer
    queryset = DealType.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser,)

    def perform_create(self, serializer):
        return serializer.save()

    def get_queryset(self):
        return self.queryset.all()


class MainRoomDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = MainRoomSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdminUser,)
    queryset = MainRoom.objects.all()
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.all()


class CategoryListAPIView(ListCreateAPIView):
    serializer_class = CreateRoomSerializer
    queryset = InvestmentRoom.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser,)

    def perform_create(self, serializer):
        return serializer.save(created_by=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)


class CategoryAllListAPIView(ListAPIView):
    serializer_class = RoomSerializer
    queryset = InvestmentRoom.objects.all()
    # permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.all()


class CategoryDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = RoomSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdminUser,)
    queryset = InvestmentRoom.objects.all()
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.all()


class UserInvestmentListAPIView(ListAPIView):
    serializer_class = serializers.UserInvestmentSerializer
    queryset = User.objects.all().order_by('-firstname')
    permission_classes = (IsAuthenticated, IsAdminUser,)
    # parser_classes = [MultiPartParser, FormParser]
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['firstname', 'lastname', 'email']
    search_fields = ['firstname', 'lastname', 'email']

    def get_queryset(self):
        return self.queryset.all()


class InvestmentListAPIView(ListAPIView):
    serializer_class = InvestmentSerializer
    queryset = Investment.objects.all().order_by('-created_at')
    permission_classes = (IsAuthenticated,)
    # parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return self.queryset.all()


class IssuerInvestmentListAPIView(ListAPIView):
    serializer_class = InvestmentSerializer
    queryset = Investment.objects.all().order_by('-created_at')
    permission_classes = (IsAuthenticated,)
    # parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class RoomInvestmentListAPIView(ListAPIView):
    serializer_class = InvestmentSerializer
    queryset = Investment.objects.all().order_by('-created_at')
    permission_classes = (IsAuthenticated,)
    # parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return self.queryset.filter(room__main_room__slug=self.kwargs['slug'])


class InvestmentDetailAPIView(RetrieveAPIView):
    serializer_class = InvestmentDetailsSerializer
    gallery_serializer = GallerySerializer
    queryset = Investment.objects.all()
    permission_classes = (IsAuthenticated,)
    parser_classes = [MultiPartParser, FormParser]
    lookup_field = 'slug'

    def get_queryset(self):
        return self.queryset.all()


class InvestmentRoomAPIView(ListAPIView):
    serializer_class = InvestmentRoomSerializer
    #serializer_all = InvestmentRoomSerializer
    gallery_serializer = GallerySerializer
    queryset = Investment.objects.all().order_by('-created_at')
    permission_classes = (IsAuthenticated,)
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['room__slug', 'risk__risk', ]

    def get_queryset(self):
        return self.queryset.all()


class GalleryAPIView(generics.GenericAPIView):
    serializer_class = GallerySerializer
    serializerud_class = GalleryUDSerializer
    permission_classes = (IsAuthenticated, IsAdminUser,)
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self, id):
        try:
            return Investment.objects.get(id=id)
        except Investment.DoesNotExist:
            raise Http404

    def get_image_object(self, id):
        try:
            return Gallery.objects.get(id=id)
        except Investment.DoesNotExist:
            raise Http404

    def post(self, request):
        snippet = self.get_object(request.data.get('investment'))
        if request.data.get('gallery'):

            imagedata = {'investment': request.data.get('investment'),
                         'gallery': request.data.get('gallery'),
                         'is_featured': False}
            in_serializer = self.serializer_class(data=imagedata)
            in_serializer.is_valid(raise_exception=True)
            in_serializer.save()
            return Response(imagedata, status=status.HTTP_201_CREATED)
        '''
        galleries = dict((request.data).lists())['galleries']
        if galleries:
            arr = []
            for img in galleries:
                modified_data = modify_input_for_multiple_files(
                    request.data.get('investment'), img, False)
                file_serializer = GallerySerializer(data=modified_data)
                if file_serializer.is_valid(raise_exception=True):
                    file_serializer.save()
                    arr.append(file_serializer.data)
            return Response(arr, status=status.HTTP_201_CREATED)
            '''


class GalleryUDAPIView(generics.GenericAPIView):
    serializer_class = GallerySerializer
    permission_classes = (IsAuthenticated, IsAdminUser,)
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self, id):
        try:
            return Gallery.objects.get(id=id)
        except Gallery.DoesNotExist:
            raise Http404

    def get_investment(self, investment):
        try:
            return Investment.objects.get(id=investment)
        except Investment.DoesNotExist:
            raise Http404

    def patch(self, request, id, format=None):
        snippet = self.get_object(id)
        #check_image = self.get_investment(request.data.get('investment'))
        serializer = GalleryUpdateSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        snippet = self.get_object(id)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ApproveInvestmentAPIView(generics.GenericAPIView):
    serializer_class = InvestmentOnlySerializer
    serializer_all = InvestmentSerializer
    gallery_serializer = GallerySerializer
    permission_classes = (IsAuthenticated, IsAdminUser,)

    def get_object(self, pk):
        try:
            return Investment.objects.get(id=pk)
        except Investment.DoesNotExist:
            raise Http404

    def patch(self, request, id, format=None):
        snippet = self.get_object(id)
        isdata = {'is_verified': request.data.get('is_verified')}
        serializer = ApproveInvestmentSerializer(snippet, data=isdata)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InvestmentAPIView(generics.GenericAPIView):
    serializer_class = InvestmentOnlySerializer
    serializer_all = InvestmentSerializer
    gallery_serializer = GallerySerializer
    permission_classes = (IsAuthenticated, IsAdminUser,)
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self, pk):
        try:
            return Investment.objects.get(pk=pk)
        except Investment.DoesNotExist:
            raise Http404

    def post(self, request):
        indata = {
            # 'owner': self.request.user,
            'name': request.data.get('name'),
            'description': request.data.get('description'),
            'room': request.data.get('room'),
            'period': request.data.get('period'),
            'video': request.data.get('video'),
            'dealtype': request.data.get('dealtype'),
            'roi': request.data.get('roi'),
            'volume': request.data.get('volume'),
            'only_returns': request.data.get('only_returns'),
            'off_plan': request.data.get('only_returns'),
            'outright_purchase': request.data.get('only_returns'),
            'outright_purchase_amount': request.data.get('outright_purchase_amount'),
            'currency': request.data.get('currency'),
            'periodic_payment': request.data.get('periodic_payment'),
            'offer_price': request.data.get('offer_price'),
            'spot_price': request.data.get('spot_price'),
            'unit_price': request.data.get('unit_price'),
            'location': request.data.get('location'),
            'annualized': request.data.get('annualized'),
            'risk': request.data.get('risk'),
            'amount': request.data.get('amount'),
            'features': request.data.get('features'),
            'is_verified': False,
            'is_closed': False,
            'owner': self.request.user.id,
            'start_date': request.data.get('start_date'),
            'end_date': request.data.get('end_date'),
            'project_cost': request.data.get('project_cost'),
            'project_raise': request.data.get('project_raise'),
            'milestone': request.data.get('milestone'),
            'minimum_allotment': request.data.get('minimum_allotment'),
            'maximum_allotment': request.data.get('maximum_allotment'),
            'offer_period': request.data.get('offer_period'),
        }
        serializer = self.serializer_class(data=indata)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        investment_data = serializer.data
        imagedata = {'investment': investment_data['id'],
                     'gallery': request.data.get('gallery'),
                     'is_featured': True}
        in_serializer = self.gallery_serializer(data=imagedata)
        in_serializer.is_valid(raise_exception=True)
        in_serializer.save()
        #images = dict((request.data).lists())['image']
        if request.data.get('galleries_1'):
            imagedata = {'investment': investment_data['id'],
                         'gallery': request.data.get('galleries_1'),
                         'is_featured': False}
            in_serializer = self.gallery_serializer(data=imagedata)
            in_serializer.is_valid(raise_exception=True)
            in_serializer.save()
        if request.data.get('galleries_2'):
            imagedata = {'investment': investment_data['id'],
                         'gallery': request.data.get('galleries_2'),
                         'is_featured': False}
            in_serializer = self.gallery_serializer(data=imagedata)
            in_serializer.is_valid(raise_exception=True)
            in_serializer.save()
        if request.data.get('galleries_3'):
            imagedata = {'investment': investment_data['id'],
                         'gallery': request.data.get('galleries_3'),
                         'is_featured': False}
            in_serializer = self.gallery_serializer(data=imagedata)
            in_serializer.is_valid(raise_exception=True)
            in_serializer.save()
        if request.data.get('galleries_4'):
            imagedata = {'investment': investment_data['id'],
                         'gallery': request.data.get('galleries_4'),
                         'is_featured': False}
            in_serializer = self.gallery_serializer(data=imagedata)
            in_serializer.is_valid(raise_exception=True)
            in_serializer.save()
        '''galleries = dict((request.data).lists())['galleries']
        if galleries:
            arr = []
            for gallery in galleries:
                modified_data = modify_input_for_multiple_files(
                    investment_data['id'], gallery, False)
                file_serializer = GallerySerializer(data=modified_data)
                file_serializer.is_valid(raise_exception=True)
                file_serializer.save()'''
        return Response(indata, status=status.HTTP_201_CREATED)


class InvestmentUDAPIView(generics.GenericAPIView):
    serializer_class = InvestmentOnlySerializer
    serializer_all = InvestmentSerializer
    gallery_serializer = GallerySerializer
    permission_classes = (IsAuthenticated, IsAdminUser,)
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self, pk):
        try:
            return Investment.objects.get(id=pk)
        except Investment.DoesNotExist:
            raise Http404

    def put(self, request, id, format=None):
        snippet = self.get_object(id)
        indata = {
            'name': request.data.get('name'),
            'description': request.data.get('description'),
            'amount': request.data.get('amount'),
            'location': request.data.get('location'),
            'room': request.data.get('room'),
            'period': request.data.get('period'),
            'roi': request.data.get('roi'),
            'risk': request.data.get('risk'),
            'periodic_payment': request.data.get('periodic_payment'),
            'annualized': request.data.get('annualized'),
            'features': request.data.get('features'),
            'is_verified': request.data.get('is_verified'),
            'is_closed': request.data.get('is_closed'),
            'video': request.data.get('video'),
            'dealtype': request.data.get('dealtype'),
            'volume': request.data.get('volume'),
            'only_returns': request.data.get('only_returns'),
            'off_plan': request.data.get('only_returns'),
            'outright_purchase': request.data.get('only_returns'),
            'outright_purchase_amount': request.data.get('outright_purchase_amount'),
            'currency': request.data.get('currency'),
            'offer_price': request.data.get('offer_price'),
            'spot_price': request.data.get('spot_price'),
            'unit_price': request.data.get('unit_price'),
            'start_date': request.data.get('start_date'),
            'end_date': request.data.get('end_date'),
            'project_cost': request.data.get('project_cost'),
            'project_raise': request.data.get('project_raise'),
            'milestone': request.data.get('milestone'),
            'minimum_allotment': request.data.get('minimum_allotment'),
            'maximum_allotment': request.data.get('maximum_allotment'),
            'offer_period': request.data.get('offer_period'),
        }
        serializer = InvestmentOnlySerializer(snippet, data=indata)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VerifyInvestmentAPIView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, IsAdminUser,)

    def get_object(self, pk):
        try:
            return Investment.objects.get(id=pk)
        except Investment.DoesNotExist:
            raise Http404

    def patch(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = ApproveInvestmentSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CloseInvestmentAPIView(generics.GenericAPIView):
    serializer_class = CloseInvestmentSerializer
    permission_classes = (IsAuthenticated, IsAdminUser,)

    def get_object(self, id):
        try:
            return Investment.objects.get(id=id)
        except Investment.DoesNotExist:
            raise Http404

    def patch(self, request, id, format=None):
        snippet = self.get_object(id)
        serializer = CloseInvestmentSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TotalInvesmentAmountAPIView(generics.GenericAPIView):
    serializer_class = TotalInvestmentSerializer
    # permission_classes = (IsAuthenticated)

    def get(self, format=None):

        queryset = list(Investment.objects.all())
        querys = Investment.objects.aggregate(amount=Sum('amount'))
        # data = queryset + querys
        #serializer = TotalInvestmentSerializer(querys, many=True)
        # print(serializer.data)
        # return Response(serializer.data)
        #combine = chain(querys, queryset)
        return Response(querys, status=status.HTTP_200_OK)
        # HttpResponse(json.dumps(something))
        #json_str = json.dumps({'amount': querys})
        # return JsonResponse(json_str, safe=False, status=status.HTTP_200_OK)


class InvestmentsByInvestorAPIView(generics.GenericAPIView):
    serializer_class = TotalInvestmentSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, format=None):

        item = Investors.objects.filter(
            is_approved=True, investor=self.request.user.id).count()
        if item:
            return Response({"investments": item}, status=status.HTTP_200_OK)
        else:
            return Response({"investments": "0",  "error": "No verified investment"},
                            status=status.HTTP_200_OK)


class InvestmentsByInvestorNAPIView(generics.GenericAPIView):
    serializer_class = TotalInvestmentSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, format=None):

        item = Investors.objects.filter(
            is_approved=False, investor=self.request.user.id).count()
        if item:
            return Response({"pendingInvestments": item}, status=status.HTTP_200_OK)
        else:
            return Response({"pendingInvestments": "0",  "error": "No verified investment"},
                            status=status.HTTP_200_OK)


class TotalReturnsAPIView(generics.GenericAPIView):
    serializer_class = TotalInvestmentSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, format=None):

        ngn = Investors.objects.filter(
            investor=self.request.user.id, investment__currency__name='NGN', is_approved=True).aggregate(NGN=Sum((F('investment__roi') / 100 * F('amount')) + F('amount')))
        usd = Investors.objects.filter(
            investor=self.request.user.id, investment__currency__name='USD', is_approved=True).aggregate(USD=Sum((F('investment__roi') / 100 * F('amount')) + F('amount')))
        gbp = Investors.objects.filter(
            investor=self.request.user.id, investment__currency__name='GBP', is_approved=True).aggregate(GBP=Sum((F('investment__roi') / 100 * F('amount')) + F('amount')))
        euro = Investors.objects.filter(
            investor=self.request.user.id, investment__currency__name='EURO', is_approved=True).aggregate(EURO=Sum((F('investment__roi') / 100 * F('amount')) + F('amount')))

        ab = {**ngn, **usd, **gbp, **euro}
        return Response(ab, status=status.HTTP_200_OK)


class TotalAmountInvestedAPIView(generics.GenericAPIView):
    serializer_class = TotalInvestmentSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, format=None):

        ngn = Investors.objects.filter(
            investor=self.request.user.id, investment__currency__name='NGN', is_approved=True).aggregate(NGN=Sum(F('amount')))
        usd = Investors.objects.filter(
            investor=self.request.user.id, investment__currency__name='USD', is_approved=True).aggregate(USD=Sum(F('amount')))
        gbp = Investors.objects.filter(
            investor=self.request.user.id, investment__currency__name='GBP', is_approved=True).aggregate(GBP=Sum(F('amount')))
        euro = Investors.objects.filter(
            investor=self.request.user.id, investment__currency__name='EURO', is_approved=True).aggregate(EURO=Sum(F('amount')))

        ab = {**ngn, **usd, **gbp, **euro}
        return Response(ab, status=status.HTTP_200_OK)


class TotalVerifiedInvesmentAmountAPIView(generics.GenericAPIView):
    serializer_class = TotalInvestmentSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, format=None):

        item = Investment.objects.filter(
            is_verified=True).aggregate(amount=Sum('amount'))
        if item:
            return Response(item, status=status.HTTP_200_OK)
        else:
            return Response({"amount": "0",  "error": "Object with referral code does not exists"},
                            status=status.HTTP_200_OK)


class TotalAmountRaiseAPIView(generics.GenericAPIView):
    serializer_class = TotalInvestmentSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, format=None):

        item = Investment.objects.filter(
            is_verified=True).aggregate(amount=Sum('project_raise'))
        if item:
            return Response(item, status=status.HTTP_200_OK)
        else:
            return Response({"amount": "0",  "error": "Object with referral code does not exists"},
                            status=status.HTTP_200_OK)


class TotalAmountReceivedAPIView(generics.GenericAPIView):
    serializer_class = TotalInvestmentSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, format=None):

        item = Investors.objects.filter(
            is_approved=True).aggregate(amount=Sum('amount'))
        if item:
            return Response(item, status=status.HTTP_200_OK)
        else:
            return Response({"amount": "0",  "error": "Object with referral code does not exists"},
                            status=status.HTTP_200_OK)


class TotalNVerifiedInvesmentAmountAPIView(generics.GenericAPIView):
    serializer_class = TotalInvestmentSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, format=None):

        item = Investment.objects.filter(
            is_verified=False).aggregate(amount=Sum('amount'))
        if item:
            return Response(item, status=status.HTTP_200_OK)
        else:
            return Response({"amount": "0",  "error": "Object with referral code does not exists"},
                            status=status.HTTP_200_OK)


class TotalVerifiedInvesmentsAPIView(generics.GenericAPIView):
    serializer_class = TotalInvestmentSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, format=None):

        item = Investment.objects.filter(
            is_verified=True).count()
        if item:
            return Response({"investments": item}, status=status.HTTP_200_OK)
        else:
            return Response({"investments": "0",  "error": "No verified investment"},
                            status=status.HTTP_200_OK)


class TotalNVerifiedInvesmentsAPIView(generics.GenericAPIView):
    serializer_class = TotalInvestmentSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, format=None):

        item = Investment.objects.filter(
            is_verified=False).count()
        if item:
            return Response({"investments": item}, status=status.HTTP_200_OK)
        else:
            return Response({"invesments": "0",  "error": "No un-verified investment"},
                            status=status.HTTP_200_OK)


class AdminExportInvestmentAPIView(generics.GenericAPIView):
    serializer_class = InvestmentSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get_serializer(self, queryset, many=True):
        return self.serializer_class(
            queryset,
            many=many,
        )

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="investment_export.csv"'

        serializer = self.get_serializer(
            Investment.objects.all(),
            many=True
        )
        header = InvestmentSerializer.Meta.fields

        writer = csv.DictWriter(response, fieldnames=header)
        writer.writeheader()
        for row in serializer.data:
            writer.writerow(row)

        return response


class IssuerCreateSponsorAPIView(generics.GenericAPIView):
    serializer_class = SponsorSerializer
    serializer_s_class = SponsorInvestmentSerializer
    permission_classes = (IsAuthenticated)
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self, pk):
        try:
            return Investment.objects.get(id=pk)
        except Investment.DoesNotExist:
            raise Http404

    def post(self, request, id, *args, **kwargs):
        checkInvestment = self.get_object(id)
        checkSponsorExist = checkSponsored(id)
        if checkSponsorExist:
            return Response({"error": "Investment already have an sponsor"},
                            status=status.HTTP_400_BAD_REQUEST)
        getSponsor = getSponsorId(request.data.get('nin'))
        # print(getSponsor)
        if getSponsor:
            query = Sponsor.objects.filter(
                nin=getSponsorId(request.data.get('nin'))).values_list('id', flat=True)[0]
            sponsorId = int(query)

        else:
            newSponsorData = {
                'nin': request.data.get('nin'),
                'name': request.data.get('name'),
                'dob': request.data.get('dob'),
                'address': request.data.get('address'),
                'identity': request.data.get('identity'),
                'phone': request.data.get('phone'),
            }
            serializer = self.serializer_class(data=newSponsorData)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            sponsorData = serializer.data
            sponsorId = sponsorData['id']

        sponsorInvestmentData = {
            'investment': id,
            'sponsor': sponsorId,
        }
        serializer_s = self.serializer_s_class(data=sponsorInvestmentData)
        serializer_s.is_valid(raise_exception=True)
        serializer_s.save()

        return Response(serializer_s.data, status=status.HTTP_201_CREATED)


class UpdateSponsorAPIView(generics.GenericAPIView):
    serializer_class = UpdateSponsorSerializer
    serializer_s_class = SponsorInvestmentSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self, pk):
        try:
            return Sponsor.objects.get(id=pk)
        except Sponsor.DoesNotExist:
            raise Http404

    def patch(self, request, id):
        checkInvestment = self.get_object(id)
        newSponsorData = {
            'name': request.data.get('name'),
            'dob': request.data.get('dob'),
            'address': request.data.get('address'),
            'identity': request.data.get('identity'),
            'phone': request.data.get('phone'),
            'is_verified': request.data.get('is_verified'),
        }
        serializer = self.serializer_class(
            checkInvestment, data=newSponsorData)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class ApproveSponsorAPIView(generics.GenericAPIView):
    serializer_class = ApproveSponsorSerializer
    permission_classes = (IsAuthenticated, IsAdminUser,)

    def get_object(self, id):
        try:
            return Sponsor.objects.get(id=id)
        except Sponsor.DoesNotExist:
            raise Http404

    def patch(self, request, id, format=None):
        snippet = self.get_object(id)
        serializer = ApproveSponsorSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SponsorListAPIView(ListAPIView):
    serializer_class = SponsorListSerializer
    queryset = Sponsor.objects.all().order_by('-created_at')
    permission_classes = (IsAuthenticated, IsAdminUser,)
    # parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return self.queryset.all()


class SponsorInvestmentsListAPIView(ListAPIView):
    serializer_class = ListSponsorInvestmentSerializer
    queryset = SponsorInvestment.objects.all().order_by('-created_at')
    permission_classes = (IsAuthenticated,)
    # parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return self.queryset.filter(sponsor=self.kwargs['id'])


class IssuerAPIView(generics.GenericAPIView):
    serializer_class = IssuerOnlySerializer
    file_serializer_class = FileUploadSerializer
    gallery_serializer = GallerySerializer
    register_serializer_class = RegisterSerializer
    profile_serializer_class = ProfileSerializer
    investor_serializer_class = IssuerInvestorSerializer
    permission_classes = (IsAuthenticated,)
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        newInvestorData = {
            'owner': self.request.user.id,
            'name': request.data.get('name'),
            'description': request.data.get('description'),
            'location': request.data.get('location'),
            'volume': request.data.get('volume'),
            'video': request.data.get('video'),
            'currency': 1,
            'dealtype': 1,
            'room': 1,
            'period': 1,
            'title_status': request.data.get('title_status'),
            'construction_status': request.data.get('construction_status'),
            'project_status': request.data.get('project_status'),
            'risk': 1,
            'features': request.data.get('features'),
            'start_date': request.data.get('start_date'),
            'end_date': request.data.get('end_date'),

        }
        serializer = self.serializer_class(data=newInvestorData)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        investment_data = serializer.data
        imagedata = {'investment': investment_data['id'],
                     'gallery': request.data.get('gallery'),
                     'is_featured': True}
        in_serializer = self.gallery_serializer(data=imagedata)
        in_serializer.is_valid(raise_exception=True)
        in_serializer.save()
        #images = dict((request.data).lists())['image']
        if request.data.get('galleries_1'):
            imagedata = {'investment': investment_data['id'],
                         'gallery': request.data.get('galleries_1'),
                         'is_featured': False}
            in_serializer = self.gallery_serializer(data=imagedata)
            in_serializer.is_valid(raise_exception=True)
            in_serializer.save()
        if request.data.get('galleries_2'):
            imagedata = {'investment': investment_data['id'],
                         'gallery': request.data.get('galleries_2'),
                         'is_featured': False}
            in_serializer = self.gallery_serializer(data=imagedata)
            in_serializer.is_valid(raise_exception=True)
            in_serializer.save()
        if request.data.get('galleries_3'):
            imagedata = {'investment': investment_data['id'],
                         'gallery': request.data.get('galleries_3'),
                         'is_featured': False}
            in_serializer = self.gallery_serializer(data=imagedata)
            in_serializer.is_valid(raise_exception=True)
            in_serializer.save()
        if request.data.get('galleries_4'):
            imagedata = {'investment': investment_data['id'],
                         'gallery': request.data.get('galleries_4'),
                         'is_featured': False}
            in_serializer = self.gallery_serializer(data=imagedata)
            in_serializer.is_valid(raise_exception=True)
            in_serializer.save()

        # Upload new investors
        if request.data.get('investors'):
            # file_serializer = self.file_serializer_class(
            #    data=request.data.get('investors'))
            # file_serializer.is_valid(raise_exception=True)
            #file = file_serializer.validated_data['file']

            csv_file = request.data.get('investors')
            if not csv_file.name.endswith('.csv'):
                messages.warning(request, 'The wrong file type was uploaded')
                return Response({"error": "The wrong file was uploaded"},
                                status=status.HTTP_400_BAD_REQUEST)
                # return HttpResponseRedirect(request.path_info)

            reader = pd.read_csv(request.data.get('investors'))

            file_data = csv_file.read().decode("utf-8")
            csv_data = file_data.split("\n")
            investmentID = investment_data['id']

            for _, fields in reader.iterrows():
                #fields = x.split(",")

                checkUser = checkNin(fields[6])
                # print(checkUser)
                if not checkUser:
                    # Check if investor is already subscribed to this investment
                    userd = str(username_generator())
                    newUserData = {
                        'firstname': fields["firstname"],
                        'lastname': fields["lastname"],
                        'username': userd,
                        'address': fields["address"],
                        'email': fields["email"],
                        'password': fields["firstname"] + fields["lastname"]+userd,
                        'referral_code': str(referral_generator()),
                        'phone': fields["phone"],
                    }
                    register_serializer = self.register_serializer_class(
                        data=newUserData)
                    register_serializer.is_valid(raise_exception=True)
                    register_serializer.save()
                    investment_data = register_serializer.data
                    #csv_file = request.data.get.FILES["csv_upload"]

                    userData = register_serializer.data
                    investorId = userData['id']

                    user = User.objects.get(email=fields["email"])
                    email_body = 'Hi '+user.firstname + \
                        ' Your email address is: ' + fields["email"] + \
                        ' Your default password to yieldroom is: \n' + \
                        fields["firstname"] + \
                        fields["lastname"]+userd + '\n' +\
                        'https://yield-room.netlify.com'
                    data = {'email_body': email_body, 'to_email': user.email,
                            'email_subject': 'Welcome to yieldroom '}
                    sender(data['email_subject'], data['email_body'],
                           'ssn@nairametrics.com', [data['to_email']])

                    Util.send_email(data)
                    print("dob")
                    print("dob")

                    newUserProfile = {
                        'user': investorId,
                        'next_of_kin': fields["next_of_kin"],
                        'nin': fields["nin"],
                        'dob': fields["dob"],
                    }
                    serializer_p = self.profile_serializer_class(
                        data=newUserProfile)
                    serializer_p.is_valid(raise_exception=True)
                    serializer_p.save()

                else:
                    checkInvestorInvestmentExist = checkInvestorExist(
                        fields["nin"], investmentID)
                    if checkInvestorInvestmentExist:
                        return Response({"error": "This investor is already subscribed to this portfolio"},
                                        status=status.HTTP_400_BAD_REQUEST)
                    else:
                        investorId = getInvestorId(fields["nin"])

                investorData = {
                    'investment': investmentID,
                    'investor': investorId,
                    'house_number': fields["house_number"],
                    'volume': fields["volume"],
                    'slug': str(investor_slug()),
                    'serialkey': str(serial_investor()),
                    'investment_type': 'off plan'

                }
                serializer_i = self.investor_serializer_class(
                    data=investorData)
                serializer_i.is_valid(raise_exception=True)
                serializer_i.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class IssuerAPIOldView(generics.GenericAPIView):
    serializer_class = IssuerOnlySerializer
    file_serializer_class = FileUploadSerializer
    gallery_serializer = GallerySerializer
    register_serializer_class = RegisterSerializer
    profile_serializer_class = ProfileSerializer
    investor_serializer_class = IssuerInvestorSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        newInvestorData = {
            'owner': self.request.user.id,
            'name': request.data.get('name'),
            'description': request.data.get('description'),
            'location': request.data.get('location'),
            'volume': request.data.get('volume'),
            'video': request.data.get('video'),
            'currency': 1,
            'dealtype': 1,
            'room': 1,
            'period': 1,
            'title_status': request.data.get('title_status'),
            'construction_status': request.data.get('construction_status'),
            'project_status': request.data.get('project_status'),
            'risk': 1,
            'features': request.data.get('features'),
            'start_date': request.data.get('start_date'),
            'end_date': request.data.get('end_date'),

        }
        serializer = self.serializer_class(data=newInvestorData)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        investment_data = serializer.data
        imagedata = {'investment': investment_data['id'],
                     'gallery': request.data.get('gallery'),
                     'is_featured': True}
        in_serializer = self.gallery_serializer(data=imagedata)
        in_serializer.is_valid(raise_exception=True)
        in_serializer.save()
        #images = dict((request.data).lists())['image']
        if request.data.get('galleries_1'):
            imagedata = {'investment': investment_data['id'],
                         'gallery': request.data.get('galleries_1'),
                         'is_featured': False}
            in_serializer = self.gallery_serializer(data=imagedata)
            in_serializer.is_valid(raise_exception=True)
            in_serializer.save()
        if request.data.get('galleries_2'):
            imagedata = {'investment': investment_data['id'],
                         'gallery': request.data.get('galleries_2'),
                         'is_featured': False}
            in_serializer = self.gallery_serializer(data=imagedata)
            in_serializer.is_valid(raise_exception=True)
            in_serializer.save()
        if request.data.get('galleries_3'):
            imagedata = {'investment': investment_data['id'],
                         'gallery': request.data.get('galleries_3'),
                         'is_featured': False}
            in_serializer = self.gallery_serializer(data=imagedata)
            in_serializer.is_valid(raise_exception=True)
            in_serializer.save()
        if request.data.get('galleries_4'):
            imagedata = {'investment': investment_data['id'],
                         'gallery': request.data.get('galleries_4'),
                         'is_featured': False}
            in_serializer = self.gallery_serializer(data=imagedata)
            in_serializer.is_valid(raise_exception=True)
            in_serializer.save()

        # Upload new investors
        if request.data.get('investors'):

            csv_file = request.data.get('investors')
            if not csv_file.name.endswith('.csv'):
                messages.warning(request, 'The wrong file type was uploaded')
                return Response({"error": "The wrong file was uploaded"},
                                status=status.HTTP_400_BAD_REQUEST)
                # return HttpResponseRedirect(request.path_info)

            file_data = csv_file.read().decode("utf-8")
            csv_data = file_data.split("\n")

            for x in csv_data:
                fields = x.split(",")

                checkUser = checkNin(fields[6])
                # print(checkUser)
                if not checkUser:
                    # Check if investor is already subscribed to this investment
                    userd = str(username_generator())
                    newUserData = {
                        'firstname': fields[0],
                        'lastname': fields[1],
                        'username': userd,
                        'address': fields[3],
                        'email': fields[2],
                        'password': fields[0] + fields[1]+userd,
                        'referral_code': str(referral_generator()),
                        'phone': fields[4],
                    }
                    register_serializer = self.register_serializer_class(
                        data=newUserData)
                    register_serializer.is_valid(raise_exception=True)
                    register_serializer.save()
                    investment_data = register_serializer.data
                    #csv_file = request.data.get.FILES["csv_upload"]

                    userData = register_serializer.data
                    investorId = userData['id']

                    user = User.objects.get(email=fields[2])
                    email_body = 'Hi '+user.firstname + \
                        ' Your email address is: ' + fields[2] + \
                        ' Your default password to yieldroom is: \n' + \
                        fields[0] + \
                        fields[1]+userd + '\n' +\
                        'https://yield-room.netlify.com'
                    data = {'email_body': email_body, 'to_email': user.email,
                            'email_subject': 'Welcome to yieldroom '}
                    sender(data['email_subject'], data['email_body'],
                           'ssn@nairametrics.com', [data['to_email']])

                    Util.send_email(data)
                    print("dob")
                    print(fields[0])
                    print(fields[1])
                    print(fields[2])
                    print(fields[3])
                    print(fields[4])
                    print(fields[5])
                    print(fields[6])
                    print(fields[7])
                    print(fields[8])
                    print("dob")

                    newUserProfile = {
                        'user': investorId,
                        'next_of_kin': fields[5],
                        'nin': fields[6],
                        'dob': fields[7],
                    }
                    serializer_p = self.profile_serializer_class(
                        data=newUserProfile)
                    serializer_p.is_valid(raise_exception=True)
                    serializer_p.save()

                else:
                    checkInvestorInvestmentExist = checkInvestorExist(
                        fields[6], id)
                    if checkInvestorInvestmentExist:
                        return Response({"error": "This investor is already subscribed to this portfolio"},
                                        status=status.HTTP_400_BAD_REQUEST)
                    else:
                        investorId = getInvestorId(fields[6])

                investorData = {
                    'investment': id,
                    'investor': investorId,
                    'house_number': fields[8],
                    'volume': fields[9],
                    'slug': str(investor_slug()),
                    'serialkey': str(serial_investor()),
                    'investment_type': 'off plan'

                }
                serializer_i = self.investor_serializer_class(
                    data=investorData)
                serializer_i.is_valid(raise_exception=True)
                serializer_i.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class IssuerCreateInvestorAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    profile_serializer_class = ProfileSerializer
    investor_serializer_class = IssuerInvestorSerializer
    register_serializer_class = SponsorInvestmentSerializer
    permission_classes = (IsAuthenticated,)
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self, pk):
        try:
            return Investment.objects.get(id=pk)
        except Investment.DoesNotExist:
            raise Http404

    def post(self, request, id, *args, **kwargs):
        checkInvestment = self.get_object(id)
        checkUser = checkNin(request.data.get('nin'))
        # print(checkUser)
        if not checkUser:
            # Check if investor is already subscribed to this investment
            userd = str(username_generator())
            newUserData = {
                'firstname': request.data.get('firstname'),
                'lastname': request.data.get('lastname'),
                'username': userd,
                'address': request.data.get('address'),
                'email': request.data.get('email'),
                'password': request.data.get('firstname') + request.data.get('lastname')+userd,
                'referral_code': str(referral_generator()),
                'phone': request.data.get('phone'),
            }
            serializer = self.serializer_class(data=newUserData)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            investment_data = serializer.data
            #csv_file = request.data.get.FILES["csv_upload"]

            userData = serializer.data
            investorId = userData['id']

            user = User.objects.get(email=userData['email'])
            email_body = 'Hi '+user.firstname + \
                ' Your email address is: ' + request.data.get('email') + \
                ' Your default password to yieldroom is: \n' + \
                request.data.get('firstname') + \
                request.data.get('lastname')+userd + '\n' +\
                'https://yield-room.netlify.com'
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Welcome to yieldroom '}
            sender(data['email_subject'], data['email_body'],
                   'ssn@nairametrics.com', [data['to_email']])

            Util.send_email(data)
            newUserProfile = {
                'identity': request.data.get('identity'),
                'user': investorId,
                'next_of_kin': request.data.get('next_of_kin'),
                'nin': request.data.get('nin'),
                'dob': request.data.get('dob'),
            }
            serializer_p = self.profile_serializer_class(data=newUserProfile)
            serializer_p.is_valid(raise_exception=True)
            serializer_p.save()

        else:
            checkInvestorInvestmentExist = checkInvestorExist(
                request.data.get('nin'), id)
            if checkInvestorInvestmentExist:
                return Response({"error": "This investor is already subscribed to this portfolio"},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                investorId = getInvestorId(request.data.get('nin'))

        investorData = {
            'investment': id,
            'investor': investorId,
            'house_number': request.data.get('house_number'),
            'volume': request.data.get('volume'),
            'slug': str(investor_slug()),
            'serialkey': str(serial_investor()),
            'investment_type': 'off plan'

        }
        serializer_i = self.investor_serializer_class(data=investorData)
        serializer_i.is_valid(raise_exception=True)
        serializer_i.save()

        return Response(serializer_i.data, status=status.HTTP_201_CREATED)


class AdminIssuerRemoveInvestorAPIView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, IsAdminUser)
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self, pk):
        try:
            return Investment.objects.get(id=pk)
        except Investment.DoesNotExist:
            raise Http404

    def post(self, request, id, *args, **kwargs):
        checkInvestment = self.get_object(id)
        checkInvestorExist = checkInvestorInvestment(
            id, request.data.get('id'))
        if checkInvestorExist:
            investor = Investors.objects.get(id=id)
            investor.delete()
            return Response({"success": "Investor has been removed"},
                            status=status.HTTP_200_OK)
        else:
            return Response({"error": "Investor is not a subscriber to this portfolio"},
                            status=status.HTTP_400_BAD_REQUEST)


class IssuerRemoveInvestorAPIView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated)
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self, pk):
        try:
            return Investment.objects.get(id=pk)
        except Investment.DoesNotExist:
            raise Http404

    def post(self, request, id, *args, **kwargs):
        checkInvestment = self.get_object(id)
        checkOwnerInvestment = checkInvestmentOwner(request.user.id, id)
        if not checkOwnerInvestment:
            return Response({"error": "Bad request"},
                            status=status.HTTP_400_BAD_REQUEST)
        checkInvestorExist = checkInvestorInvestment(
            id, request.data.get('id'))
        if checkInvestorExist:
            investor = Investors.objects.get(id=id)
            investor.delete()
            return Response({"success": "Investor has been removed"},
                            status=status.HTTP_200_OK)
        else:
            return Response({"error": "Investor is not a subscriber to this portfolio"},
                            status=status.HTTP_400_BAD_REQUEST)


class IssuerSummaryAPIView(generics.GenericAPIView):
    serializer_class = TotalInvestmentSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, format=None):

        countInvestors = Investors.objects.filter(
            investment__owner=self.request.user.id).count()
        if countInvestors:
            totalInvestors = countInvestors
        else:
            totalInvestors = 0

        countInvestments = Investment.objects.filter(
            owner=self.request.user.id).count()
        if countInvestments:
            totalInvestments = countInvestments
        else:
            totalInvestments = 0

        countSponsors = SponsorInvestment.objects.filter(
            investment__owner=self.request.user.id).count()
        if countSponsors:
            totalSposnors = countSponsors
        else:
            totalSposnors = 0

        return Response({"totalInvestors": totalInvestors, "totalInvestments": totalInvestments, "totalSponsors": totalSposnors}, status=status.HTTP_200_OK)
