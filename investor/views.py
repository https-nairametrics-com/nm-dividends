from django.shortcuts import render
from authentication.models import User
from investment.views import IsSuperUser
from investment.models import Installment, Investors, Investment
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView
from rest_framework import generics, status, views, permissions, filters
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from authentication.utils import serial_investor, investor_slug
from .models import Risk, Interest, InvestmentSize, Period, Expectations
from .serializers import InstallmentSerializer, InvestorExportSerializer, UserInvestorSerializer, AdminUInvestorSerializer, CreateInvestorSerializer, ApproveInvestorSerializer, CloseInvestorSerializer, InvestorSerializer, AdminInvestorSerializer, PeriodSerializer, SizeSerializer, RiskSerializer, InterestSerializer, ExpectationsSerializer
from .permissions import IsOwner, IsUserApproved
from django.db.models import Sum, Aggregate, Avg, Count
from django.http import JsonResponse, Http404, HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
import csv
# Create your views here.


def isApproved(id):
    query = User.objects.filter(id=id).values_list('is_approved', flat=True)[0]
    return query


def getInvesmentAmount(id):
    query = Investment.objects.filter(
        id=id).values_list('amount', flat=True)[0]
    return query


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
    # permission_classes = (IsAuthenticated,)
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
    # permission_classes = (IsAuthenticated,)

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
    # permission_classes = (IsAuthenticated,)

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

        if (isApproved(request.user.id) == False):
            return Response({"status": "error",  "error": "User account not approved"},
                            status=status.HTTP_400_BAD_REQUEST)
        investment_id = self.get_object(id)
        if (int(request.data.get('amount')) < getInvesmentAmount(id)):
            investordata = {
                'amount': request.data.get('amount'),
                'bid_price': request.data.get('bid_price'),
                'volume': request.data.get('volume'),
                'slug': str(investor_slug()),
                'investment': id,
                'investor': self.request.user.id,
                'serialkey': str(serial_investor()),
                'is_approved': False,
                'is_closed': False,
            }
            serializer = self.serializer_class(data=investordata)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "error",  "error": "Amount cannot exceed Invesment amount"},
                            status=status.HTTP_400_BAD_REQUEST)


class AdminInvestmentAPIView(generics.GenericAPIView):
    serializer_class = CreateInvestorSerializer
    queryset = Investors.objects.all().order_by('-created_at')
    permission_classes = (IsAuthenticated, IsAdminUser,)
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    def get_object(self, id):
        try:
            return Investment.objects.get(id=id)
        except Investment.DoesNotExist:
            raise Http404

    def get_user_object(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            raise Http404

    def post(self, request, id, format=None):

        if (isApproved(request.user.id) == False):
            return Response({"status": "error",  "error": "User account not approved"},
                            status=status.HTTP_400_BAD_REQUEST)
        investment_id = self.get_object(id)
        user_id = self.get_user_object(request.data.get('investor'))
        if (request.data.get('amount') > getInvesmentAmount(id)):

            if int(request.data.get('amount')) > request.data.get('bid_price'):
                return Response({"status": "error",  "error": "Amount cannot be greater than bid price"},
                                status=status.HTTP_400_BAD_REQUEST)
            investordata = {
                'amount': request.data.get('amount'),
                'bid_price': request.data.get('bid_price'),
                'volume': request.data.get('volume'),
                'slug': str(investor_slug()),
                'investment': id,
                'investor': request.data.get('investor'),
                'serialkey': str(serial_investor()),
                'is_approved': False,
                'is_closed': False,
            }
            serializer = self.serializer_class(data=investordata)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "error",  "error": "Amount cannot exceed Invesment amount"},
                            status=status.HTTP_400_BAD_REQUEST)


class InvestorListAPIView(ListAPIView):
    serializer_class = InvestorSerializer
    queryset = Investors.objects.all().order_by('-created_at')
    permission_classes = (IsAuthenticated, IsUserApproved, )
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    def get_queryset(self):
        return self.queryset.filter(investor=self.request.user)


class InvestorDetailAPIView(RetrieveAPIView):
    serializer_class = InvestorSerializer
    queryset = Investors.objects.all().order_by('-created_at')
    permission_classes = (IsAuthenticated, IsUserApproved,)
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.filter(investor=self.request.user)


class TotalAmountAPIView(generics.GenericAPIView):
    serializer_class = InvestorSerializer
    permission_classes = (IsAuthenticated, IsUserApproved,)

    def get(self, format=None):
        item = Investors.objects.filter(
            is_approved=True, investment__currency__name="NGN", investor=self.request.user.id).aggregate(amount=Sum('amount'))
        if item:
            return Response(item, status=status.HTTP_200_OK)
        else:
            return Response({"amount": "0",  "error": "No verified investment"},
                            status=status.HTTP_200_OK)


class TotalAmountClosedAPIView(generics.GenericAPIView):
    serializer_class = InvestorSerializer
    permission_classes = (IsAuthenticated, IsUserApproved,)

    def get(self, format=None):
        item = Investors.objects.filter(
            is_approved=True, is_closed=True, investor=self.request.user.id).aggregate(amount=Sum('amount'))
        if item:
            return Response(item, status=status.HTTP_200_OK)
        else:
            return Response({"amount": "0",  "error": "No verified investment"},
                            status=status.HTTP_200_OK)


class TotalInvestmentsAPIView(generics.GenericAPIView):
    serializer_class = InvestorSerializer
    permission_classes = (IsAuthenticated, IsUserApproved,)

    def get(self, format=None):

        item = Investors.objects.filter(
            is_approved=True).count()
        if item:
            return Response({"investments": item}, status=status.HTTP_200_OK)
        else:
            return Response({"investments": "0",  "error": "No verified investment"},
                            status=status.HTTP_200_OK)


class TotalInvestmentRoomAPIView(generics.GenericAPIView):
    serializer_class = InvestorSerializer
    permission_classes = (IsAuthenticated, IsUserApproved,)

    def get(self, format=None):

        # item = Investors.objects.filter(
        #    is_approved=True).annotate(unique_names=Count('investment', distinct=True))
        item = Investors.objects.filter(is_approved=True).values(
            'investment').distinct().count()
        if item:
            return Response(item, status=status.HTTP_200_OK)
        else:
            return Response({"investments": "0",  "error": "No verified investment"},
                            status=status.HTTP_200_OK)


class AdminInvestorListAPIView(ListAPIView):
    serializer_class = InvestorSerializer
    queryset = Investors.objects.all().order_by('-created_at')
    permission_classes = (IsAuthenticated, IsAdminUser,)
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    def get_queryset(self):
        return self.queryset.all()


class AdminSingleInvestorListAPIView(ListAPIView):
    serializer_class = InvestorSerializer
    queryset = Investors.objects.all().order_by('-created_at')
    permission_classes = (IsAuthenticated, IsAdminUser,)
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    def get_queryset(self):
        return self.queryset.filter(investor=self.kwargs['id'])
    '''
    lookup_field = "investor"

    def get(self, request, id):
        query = Investors.objects.filter(investor=id).values()
        if query.exists():
            print(query)
            ser = InvestorSerializer(query)

            return Response({"status": "success", "data": ser.data}, status=status.HTTP_200_OK)
        else:
            return Response({"res": "User has no investment"},
                            status=status.HTTP_200_OK)
    '''


class AdminInstallmentListAPIView(ListAPIView):
    serializer_class = InstallmentSerializer
    queryset = Installment.objects.all().order_by('-created_at')
    permission_classes = (IsAuthenticated, IsAdminUser,)
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    def get_queryset(self):
        return self.queryset.all()


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


class AdminUInvestorAPIView(generics.GenericAPIView):
    serializer_class = AdminUInvestorSerializer
    queryset = Investors.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser,)
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    def check_investment(self, pk):
        try:
            return Investment.objects.get(id=pk)
        except Investment.DoesNotExist:
            raise Http404

    def get_object(self, pk):
        try:
            return Investors.objects.get(id=pk)
        except Investors.DoesNotExist:
            raise Http404

    def check_user(self, pk):
        try:
            return User.objects.get(id=pk)
        except User.DoesNotExist:
            raise Http404

    def put(self, request, id, format=None):
        investment_id = self.get_object(id)
        investor = self.check_user(request.data.get('investor'))
        investment = self.check_investment(request.data.get('investment'))
        investordata = {
            'amount': request.data.get('amount'),
            'bid_price': request.data.get('bid_price'),
            'investor': request.data.get('investor'),
            'investment': request.data.get('investment'),
            'is_approved': request.data.get('is_approved'),
            'approved_by': self.request.user.id,
            'is_closed': request.data.get('is_closed'),
            'closed_by': self.request.user.id,
        }
        serializer = self.serializer_class(investment_id, data=investordata)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        snippet = self.get_object(id)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdminApproveInvestorAPIView(generics.GenericAPIView):
    serializer_class = ApproveInvestorSerializer
    queryset = Investors.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser,)
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    def check_investor(self, pk):
        try:
            return Investors.objects.get(id=pk)
        except Investors.DoesNotExist:
            raise Http404

    def patch(self, request, id, format=None):
        investment_id = self.check_investor(id)
        investordata = {
            'is_approved': request.data.get('is_approved'),
            'approved_by': self.request.user,
        }
        serializer = self.serializer_class(investment_id, data=investordata)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminCloseInvestorAPIView(generics.GenericAPIView):
    serializer_class = CloseInvestorSerializer
    queryset = Investors.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser,)
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    def check_investor(self, pk):
        try:
            return Investors.objects.get(id=pk)
        except Investors.DoesNotExist:
            raise Http404

    def patch(self, request, id, format=None):
        investment_id = self.check_investor(id)
        investordata = {
            'is_closed': request.data.get('is_closed'),
            'closed_by': self.request.user,
        }
        serializer = self.serializer_class(investment_id, data=investordata)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApproveInvestorAPIView(generics.GenericAPIView):
    serializer_class = ApproveInvestorSerializer
    queryset = Investors.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser,)
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    def get_object(self, pk):
        try:
            return Investors.objects.get(id=pk)
        except Investors.DoesNotExist:
            raise Http404

    def patch(self, request, id, format=None):
        investment_id = self.get_object(id)
        investordata = {
            'is_approved': request.data.get('is_approved'),
            'approved_by': self.request.user.id,
        }
        serializer = self.serializer_class(investment_id, data=investordata)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CloseInvestorAPIView(generics.GenericAPIView):
    serializer_class = CloseInvestorSerializer
    queryset = Investors.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser,)
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    def get_object(self, pk):
        try:
            return Investors.objects.get(id=pk)
        except Investors.DoesNotExist:
            raise Http404

    def patch(self, request, id, format=None):
        investment_id = self.get_object(id)
        investordata = {
            'is_closed': request.data.get('is_closed'),
            'closed_by': self.request.user.id,
        }
        serializer = self.serializer_class(investment_id, data=investordata)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExportInvestorsCount(generics.GenericAPIView):
    serializer_class = InvestorSerializer
    queryset = Investors.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'

        writer = csv.writer(response)

        for user in User.objects.all():
            approved_portfolio = Investors.objects.filter(
                investor=user.id)
            #completed_portfolio = approved_portfolio.filter(is_closed=True)

            row = ','.join([
                user.firstname,
                user.lastname
                # approved_portfolio.count()
                # completed_portfolio.count()
            ])

            writer.writerow(row)

        return response


class AdminUserInvestorListAPIView(ListAPIView):
    serializer_class = UserInvestorSerializer
    queryset = User.objects.filter(is_approved=True).order_by('-firstname')
    permission_classes = (IsAuthenticated, IsAdminUser,)
    # parser_classes = [MultiPartParser, FormParser]
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['firstname', 'lastname', 'email']
    search_fields = ['firstname', 'lastname', 'email']

    def get_queryset(self):
        return self.queryset.all()


class AdminExportInvestorAPIView(generics.GenericAPIView):
    serializer_class = InvestorExportSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get_serializer(self, queryset, many=True):
        return self.serializer_class(
            queryset,
            many=many,
        )

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="investors_export.csv"'

        serializer = self.get_serializer(
            Investors.objects.all(),
            many=True
        )
        header = InvestorExportSerializer.Meta.fields

        writer = csv.DictWriter(response, fieldnames=header)
        writer.writeheader()
        for row in serializer.data:
            writer.writerow(row)

        return response
