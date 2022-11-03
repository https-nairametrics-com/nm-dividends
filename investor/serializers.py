from rest_framework import serializers
from .models import Period, Risk, Expectations, InvestmentSize, Interest, Investor


class PeriodSerializer(serializers.ModelSerializer):

    class Meta:
        model = Period
        fields = ['id', 'period', 'is_verified',
                  'created_by']
