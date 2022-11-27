from rest_framework import serializers
from .models import InitialInterests, Period, Risk, Expectations, InvestmentSize, Interest
from investment.serializers import UserInvestmentSerializer, RoomSerializer
from investment.models import Investors, Investment
from authentication.models import User


class investmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = ['id', 'slug', 'name', 'amount', 'location', 'roi']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'firstname', 'lastname', 'username', 'referral_code']


class PeriodSerializer(serializers.ModelSerializer):

    class Meta:
        model = Period
        fields = ['id', 'period', 'is_verified',
                  ]


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


class RiskSerializer(serializers.ModelSerializer):
    #user = UserInvestmentSerializer(read_only=False)

    class Meta:
        model = Risk
        fields = ['id', 'risk', 'is_verified',
                  ]


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
    investment = investmentSerializer(many=False, read_only=False)
    investor = UserInvestmentSerializer(many=False, read_only=False)

    class Meta:
        model = Investors
        fields = ('id', 'slug', 'investment', 'investor', 'amount', 'serialkey',
                  'is_approved', 'is_closed', 'created_at')

    def get_investment(self, instance):
        return instance.geo_info.investment

    def get_investor(self, instance):
        return instance.geo_info.investor


class CreateInvestorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Investors
        fields = ('id', 'slug', 'investment', 'investor', 'amount', 'serialkey',
                  'is_approved', 'is_closed', 'created_at')


class AdminInvestorSerializer(serializers.ModelSerializer):
    investment = investmentSerializer(many=False, read_only=False)
    investor = UserInvestmentSerializer(many=False, read_only=False)
    approved_by = UserInvestmentSerializer(many=False, read_only=False)
    closed_by = UserInvestmentSerializer(many=False, read_only=False)

    class Meta:
        model = Investors
        fields = ('id', 'slug', 'investment', 'investor', 'amount', 'serialkey',
                  'is_approved', 'approved_by', 'is_closed', 'closed_by', 'created_at')

    def get_investment(self, instance):
        return instance.geo_info.investment

    def get_investor(self, instance):
        return instance.geo_info.investor

    def get_approved_by(self, instance):
        return instance.geo_info.approved_by

    def get_closed_by(self, instance):
        return instance.geo_info.closed_by
