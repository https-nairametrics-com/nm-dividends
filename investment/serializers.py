from rest_framework import serializers
from .models import Investment, InvestmentRoom, Gallery, Investors
from investor.models import Period
from authentication.models import User


class UserInvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'firstname', 'lastname']


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
    image_url = serializers.SerializerMethodField('get_image_url')

    class Meta:
        model = Gallery
        fields = ['id', 'investment', 'gallery',
                  'is_featured', 'image_url']

        def get_image_url(self, obj):

            request = self.context.get("request")
            return request.build_absolute_uri(obj.gallery)


class InvestmentSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField('get_image_url')

    gallery_set = serializers.StringRelatedField(many=True)

    room_name = RoomSerializer()
    period_details = PeriodInvestmentSerializer(read_only=False)
    user_details = UserInvestmentSerializer(read_only=False)
    #images = GallerySerializer()

    class Meta:
        model = Investment
        fields = ['id', 'owner', 'name', 'description',
                  'amount', 'room_name', 'gallery_set', 'user_details', 'period_details', 'roi',
                  'annualized', 'risk', 'features', 'is_verified', 'image_url']

    def get_image_url(self, obj):

        request = self.context.get("request")
        return request.build_absolute_uri(obj.gallery)


class InvestmentOnlySerializer(serializers.ModelSerializer):

    class Meta:
        model = Investment
        fields = ['id', 'name', 'description',
                  'amount', 'room', 'period', 'roi',
                  'annualized', 'risk', 'features', 'is_verified']


class InvestorsSerializer(serializers.ModelSerializer):

    class Meta:
        model = InvestmentRoom
        fields = ['investment', 'id', 'investor',
                  'is_approved', 'amount', 'serialkey', 'approved_by',
                  'is_closed', 'closed_by']
