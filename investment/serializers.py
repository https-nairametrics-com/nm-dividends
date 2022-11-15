from rest_framework import serializers
from .models import Investment, InvestmentRoom, Gallery, Investors
from investor.models import Period
from authentication.models import User
from django.conf import settings


class UserInvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'firstname', 'lastname', ]


class PeriodInvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = ['period', ]


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = InvestmentRoom
        fields = ['name', 'description',
                  'is_verified', ]


class GallerySerializer(serializers.ModelSerializer):
    gallery_url = serializers.SerializerMethodField("get_image_url")
    # gallery = serializers.ImageField(
    # max_length=None, allow_empty_file=False, allow_null=False, use_url=True, required=False)

    class Meta:
        model = Gallery
        fields = ['id', 'investment', 'gallery', 'gallery_url',
                  'is_featured']

    def get_image_url(self, obj):
        return obj.gallery.url

    '''
    def get_gallery(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.gallery.url)
        '''


class InvestmentSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    #gallery_set = serializers.StringRelatedField(many=True)

    room = RoomSerializer(many=False, read_only=False)
    period = PeriodInvestmentSerializer(read_only=False)
    owner = UserInvestmentSerializer(read_only=False)
    #gallery_investment = GallerySerializer(read_only=False)

    '''
    def get_image(self, gallery):
        pesticide_qs = Gallery.objects.filter(
            gallery__investment=gallery)
        return GallerySerializer(pesticide_qs, many=True).data
        '''

    class Meta:
        model = Investment
        fields = ['id', 'owner', 'name', 'description',
                  'amount', 'room', 'roi', 'period',
                  'annualized',  'risk', 'features', 'is_verified', 'image']

    def get_image(self, obj):
        logger_queryset = Gallery.objects.filter(investment=obj.id)
        return GallerySerializer(logger_queryset, many=True).data

    '''
    def get_image_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.image_url)
        '''

    def get_room(self, instance):
        return instance.geo_info.room

    def get_owner(self, instance):
        return instance.geo_info.owner

    def get_userdetails(self, instance):
        return instance.geo_info.userdetails


class TotalInvestmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Investment
        fields = ['amount']


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
                  'is_closed', 'closed_by', ]
