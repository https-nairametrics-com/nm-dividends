from django.shortcuts import render
from authentication.models import User
from .models import InvestmentRoom, Investment, Gallery, Investors
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView
from rest_framework import filters, generics, status, views, permissions
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from authentication.utils import serial_investor
from .permissions import IsOwner, IsInvestmentOwner
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .serializers import GalleryUpdateSerializer, CloseInvestmentSerializer, GalleryUDSerializer, ApproveInvestmentSerializer, TotalInvestmentSerializer, InvestmentRoomSerializer, InvestmentOnlySerializer, RoomSerializer, GallerySerializer, InvestmentSerializer, InvestorsSerializer
from investor.serializers import RiskSerializer
from investor.models import Risk, Period, InvestmentSize, Interest
from django.db.models import Sum, Aggregate, Avg
from django.http import JsonResponse, Http404, HttpResponse
import json
from itertools import chain
from .helpers import modify_input_for_multiple_files
from decimal import *
from django_filters.rest_framework import DjangoFilterBackend
import csv
from . import serializers
# Create your views here.


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

    def get_queryset(self):
        return self.queryset.all()


class InvestmentListAPIView(ListAPIView):
    serializer_class = InvestmentSerializer
    queryset = Investment.objects.all().order_by('-created_at')
    permission_classes = (IsAuthenticated,)
    # parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return self.queryset.all()


class InvestmentDetailAPIView(RetrieveAPIView):
    serializer_class = InvestmentRoomSerializer
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
    queryset = Investment.objects.all()
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

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
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
            'roi': request.data.get('roi'),
            'location': request.data.get('location'),
            'annualized': request.data.get('annualized'),
            'risk': request.data.get('risk'),
            'amount': request.data.get('amount'),
            'features': request.data.get('features'),
            'is_verified': False,
            'is_closed': False,
        }
        serializer = self.serializer_class(data=indata)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=self.request.user)
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
            'annualized': request.data.get('annualized'),
            'features': request.data.get('features'),
            'is_verified': request.data.get('is_verified'),
            'is_closed': request.data.get('is_closed'),
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


class ExportInvestmentAPIView(generics.GenericAPIView):
    serializer_class = InvestmentSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get_serializer(self, queryset, many=True):
        return self.serializer_class(
            queryset,
            many=many,
        )

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'

        serializer = self.get_serializer(
            User.objects.all(),
            many=True
        )
        header = InvestmentSerializer.Meta.fields

        writer = csv.DictWriter(response, fieldnames=header)
        writer.writeheader()
        for row in serializer.data:
            writer.writerow(row)

        return response
