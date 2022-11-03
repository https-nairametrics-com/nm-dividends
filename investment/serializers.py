from rest_framework import serializers
from .models import Investment, InvestmentRoom, Gallery, Investors
from investor.models import Period
from authentication.models import User


class UserInvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['firstname', 'lastname']


class PeriodInvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = ['period']


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = InvestmentRoom
        fields = ['id', 'name', 'description',
                  'is_verified']


class GallerySerializer(serializers.ModelSerializer):

    class Meta:
        model = InvestmentRoom
        fields = ['investment', 'gallery',
                  'is_verified']


class InvestmentSerializer(serializers.ModelSerializer):
    room_name = RoomSerializer(read_only=False)
    period_details = PeriodInvestmentSerializer(read_only=False)
    user_details = UserInvestmentSerializer(read_only=False)
    images = GallerySerializer(read_only=False)

    class Meta:
        model = Investment
        fields = ['id', 'owner', 'name', 'description',
                  'amount', 'room_name', 'images', 'user_details', 'period', 'period_details', 'roi',
                  'annualized', 'risk', 'features', 'is_verified']


class InvestorsSerializer(serializers.ModelSerializer):

    class Meta:
        model = InvestmentRoom
        fields = ['investment', 'id', 'investor',
                  'is_approved', 'amount', 'serialkey', 'approved_by',
                  'is_closed', 'closed_by']
