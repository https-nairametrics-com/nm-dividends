from rest_framework import serializers
from .models import InitialInterests, Period, Risk, Expectations, InvestmentSize, Interest, Investor
from investment.serializers import UserInvestmentSerializer


class PeriodSerializer(serializers.ModelSerializer):

    class Meta:
        model = Period
        fields = ['id', 'period', 'is_verified',
                  ]


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentSize
        fields = ['investment_size', 'is_verified',
                  ]


class AdminSizeSerializer(serializers.ModelSerializer):
    user = UserInvestmentSerializer(read_only=False)

    class Meta:
        model = InvestmentSize
        fields = ['investment_size', 'is_verified',
                  'created_by', 'user']


class RiskSerializer(serializers.ModelSerializer):
    #user = UserInvestmentSerializer(read_only=False)

    class Meta:
        model = Risk
        fields = ['risk', 'is_verified',
                  ]


class AdminRiskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Risk
        fields = ['risk', 'is_verified', 'created_by', 'user'
                  ]


class InterestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Interest
        fields = ['interest', 'is_verified',
                  ]


class AdminInterestSerializer(serializers.ModelSerializer):
    user = UserInvestmentSerializer(read_only=False)

    class Meta:
        model = Interest
        fields = ['interest', 'is_verified', 'created_by', 'user'
                  ]


class ExpectationsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Expectations
        fields = ['expectation', 'is_verified',
                  ]


class AdminExpectationsSerializer(serializers.ModelSerializer):
    user = UserInvestmentSerializer(read_only=False)

    class Meta:
        model = Expectations
        fields = ['interest', 'is_verified', 'created_by', 'user'
                  ]


class InitialInterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = InitialInterests
        fields = ('id', 'owner', 'risk', 'period',
                  'interest', 'investmentsize')
