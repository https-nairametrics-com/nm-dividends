from rest_framework import serializers
from .models import InitialInterests, Period, Risk, Expectations, InvestmentSize, Interest
from investment.serializers import DealTypeSerializer, CurrencySerializer, UserInvestmentSerializer, RoomSerializer
from investment.models import Currency, DealType, Investors, Investment, InvestmentRoom
from authentication.models import User
from django.db.models import Sum, Aggregate, Avg
from comment.models import Comment
import decimal


class investmentSerializer(serializers.ModelSerializer):
    dealtype = DealTypeSerializer(many=False, read_only=False)
    currency = CurrencySerializer(many=False, read_only=False)

    class Meta:
        model = Investment
        fields = ['id', 'slug', 'name', 'unit_price', 'spot_price', 'offer_price',
                  'amount', 'currency', 'dealtype', 'video', 'location', 'roi']


class RiskSerializer(serializers.ModelSerializer):
    #user = UserInvestmentSerializer(read_only=False)

    class Meta:
        model = Risk
        fields = ['id', 'risk', 'is_verified',
                  ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'firstname', 'lastname',
                  'username', 'referral_code', 'phone']


class CommentSerializer(serializers.ModelSerializer):
    responded_by = UserSerializer(many=False, read_only=False)

    class Meta:
        model = Comment
        fields = ['id', 'slug', 'comment',
                  'investor', 'is_closed', 'responded_by']

    def get_responsed_by(self, instance):
        return instance.geo_info.responded_by


class UserInvestorSerializer(serializers.ModelSerializer):
    totalactiveinvestment = serializers.SerializerMethodField()
    totalpendinginvestment = serializers.SerializerMethodField()
    totalclosedinvestment = serializers.SerializerMethodField()
    totalcomment = serializers.SerializerMethodField()
    amountngn = serializers.SerializerMethodField()
    amountusd = serializers.SerializerMethodField()
    amounteuro = serializers.SerializerMethodField()
    amountgbp = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'firstname', 'lastname', 'email', 'phone', 'totalactiveinvestment', 'totalpendinginvestment', 'totalclosedinvestment', 'totalcomment',
                  'amountngn', 'amountusd', 'amounteuro', 'amountgbp', 'created_at']

    def get_totalactiveinvestment(self, obj):
        return Investors.objects.filter(investor=obj.id, is_approved=True, is_closed=False).count()
        # return GallerySerializer(logger_queryset, many=True).data

    def get_totalpendinginvestment(self, obj):
        return Investors.objects.filter(investor=obj.id, is_approved=False).count()

    def get_totalclosedinvestment(self, obj):
        return Investors.objects.filter(investor=obj.id, is_approved=True, is_closed=True).count()

    def get_totalcomment(self, obj):
        return Comment.objects.filter(investor__investor=obj.id).count()

    def get_amountngn(self, obj):
        return Investors.objects.filter(investor=obj.id, investment__currency__name='NGN').aggregate(amount=Sum('amount'))

    def get_amountusd(self, obj):
        return Investors.objects.filter(investor=obj.id, investment__currency__name='USD').aggregate(amount=Sum('amount'))

    def get_amounteuro(self, obj):
        return Investors.objects.filter(investor=obj.id, investment__currency__name='EURO').aggregate(amount=Sum('amount'))

    def get_amountgbp(self, obj):
        return Investors.objects.filter(investor=obj.id, investment__currency__name='GBP').aggregate(amount=Sum('amount'))


class PeriodSerializer(serializers.ModelSerializer):

    class Meta:
        model = Period
        fields = ['id', 'period', 'is_verified',
                  ]


class InvestmentLSerializer(serializers.ModelSerializer):
    period = PeriodSerializer(read_only=False)
    room = RoomSerializer(read_only=False)
    risk = RiskSerializer(read_only=False)
    dealtype = DealTypeSerializer(many=False, read_only=False)
    currency = CurrencySerializer(many=False, read_only=False)

    class Meta:
        model = Investment
        fields = ['id', 'slug', 'name', 'amount', 'currency', 'dealtype',
                  'volume', 'offer_price', 'spot_price', 'unit_price',
                  'location', 'roi', 'period', 'room', 'risk', 'start_date',
                  'end_date', 'created_at', 'is_verified', 'is_closed']


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentSize
        fields = ['id', 'investment_size', 'is_verified',
                  ]


class AdminSizeSerializer(serializers.ModelSerializer):
    user = UserInvestmentSerializer(read_only=False)

    class Meta:
        model = InvestmentSize
        fields = ['id', 'investment_size', 'is_verified',
                  'created_by', 'user']


class AdminRiskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Risk
        fields = ['id', 'risk', 'is_verified', 'created_by', 'user'
                  ]


class InterestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Interest
        fields = ['id', 'interest', 'is_verified',
                  ]


class AdminInterestSerializer(serializers.ModelSerializer):
    user = UserInvestmentSerializer(read_only=False)

    class Meta:
        model = Interest
        fields = ['id', 'interest', 'is_verified', 'created_by', 'user'
                  ]


class ExpectationsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Expectations
        fields = ['id', 'expectation', 'is_verified',
                  ]


class AdminExpectationsSerializer(serializers.ModelSerializer):
    user = UserInvestmentSerializer(read_only=False)

    class Meta:
        model = Expectations
        fields = ['id', 'interest', 'is_verified', 'created_by', 'user'
                  ]


class InitialInterestSerializer(serializers.ModelSerializer):
    investmentsize = SizeSerializer(read_only=False)
    interest = InterestSerializer(read_only=False)
    period = PeriodSerializer(read_only=False)
    risk = RiskSerializer(read_only=False)
    owner = UserInvestmentSerializer(read_only=False)

    class Meta:
        model = InitialInterests
        fields = ('id', 'owner', 'risk', 'period',
                  'interest', 'investmentsize')

    def get_investmentsize(self, instance):
        return instance.geo_info.investmentsize

    def get_interest(self, instance):
        return instance.geo_info.interest

    def get_period(self, instance):
        return instance.geo_info.period

    def get_risk(self, instance):
        return instance.geo_info.risk

    def get_owner(self, instance):
        return instance.geo_info.owner


class RegistrationInitialInterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = InitialInterests
        fields = ('id', 'owner', 'risk', 'period',
                  'interest', 'investmentsize')


class ApproveInvestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investors
        fields = ('id', 'approved_by', 'is_approved')


class CloseInvestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investors
        fields = ('id', 'closed_by', 'is_closed')


class InvestorSerializer(serializers.ModelSerializer):
    investment = InvestmentLSerializer(many=False, read_only=False)
    investor = UserInvestorSerializer(many=False, read_only=False)
    comment = serializers.SerializerMethodField()
    portfolio_value = serializers.SerializerMethodField()

    class Meta:
        model = Investors
        fields = ('id', 'slug', 'investment', 'investor', 'amount', 'bid_price', 'serialkey',
                  'portfolio_value', 'is_approved', 'is_closed', 'comment', 'created_at')

    def get_investment(self, instance):
        return instance.geo_info.investment

    def get_investor(self, instance):
        return instance.geo_info.investor

    def get_comment(self, obj):
        queryset = Comment.objects.filter(investor=obj.id)
        return CommentSerializer(queryset, many=True).data

    def get_portfolio_value(self, obj):
        rob = Investors.objects.filter(
            id=obj.id).values_list('investment', flat=True)[0]
        roi = Investment.objects.filter(
            id=rob).values_list('roi', flat=True)[0]
        amount = Investors.objects.filter(
            id=obj.id).values_list('amount', flat=True)[0]
        returns_on_i = ((decimal.Decimal(roi) / decimal.Decimal(100))
                        * decimal.Decimal(amount)) + decimal.Decimal(amount)
        return returns_on_i.quantize(decimal.Decimal('0.00'))


class AdminInvestorSerializer(serializers.ModelSerializer):
    investment = InvestmentLSerializer(many=False, read_only=False)
    investor = UserInvestorSerializer(many=False, read_only=False)
    comment = serializers.SerializerMethodField()

    class Meta:
        model = Investors
        fields = ('id', 'slug', 'investment', 'investor', 'amount', 'bid_price', 'serialkey',
                  'is_approved', 'is_closed', 'comment', 'created_at')

    def get_investment(self, instance):
        return instance.geo_info.investment

    def get_investor(self, instance):
        return instance.geo_info.investor

    def get_comment(self, obj):
        queryset = Comment.objects.filter(investor=obj.id)
        return CommentSerializer(queryset, many=True).data


class AdminUInvestorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Investors
        fields = ('id', 'closed_by', 'approved_by', 'investment', 'investor', 'bid_price', 'amount',
                  'is_approved', 'is_closed')


class CreateInvestorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Investors
        fields = ('id', 'slug', 'investment', 'investor', 'bid_price', 'amount', 'serialkey',
                  'is_approved', 'is_closed', 'created_at')


class AdminInvestorSerializer(serializers.ModelSerializer):
    investment = investmentSerializer(many=False, read_only=False)
    investor = UserInvestmentSerializer(many=False, read_only=False)
    approved_by = UserInvestmentSerializer(many=False, read_only=False)
    closed_by = UserInvestmentSerializer(many=False, read_only=False)

    class Meta:
        model = Investors
        fields = ('id', 'slug', 'investment', 'investor', 'bid_price', 'amount', 'serialkey',
                  'is_approved', 'approved_by', 'is_closed', 'closed_by', 'created_at', 'updated_at')

    def get_investment(self, instance):
        return instance.geo_info.investment

    def get_investor(self, instance):
        return instance.geo_info.investor

    def get_approved_by(self, instance):
        return instance.geo_info.approved_by

    def get_closed_by(self, instance):
        return instance.geo_info.closed_by
