from rest_framework import serializers
from .models import Investment, MainRoom, DealType, Currency, InvestmentRoom, Gallery, Investors
from investor.models import Period, Risk
from authentication.models import User
from django.conf import settings
from django.db.models import Sum, Aggregate, Avg


class UserInvestmentSerializer(serializers.ModelSerializer):
    totalinvestment = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'firstname', 'phone',
                  'lastname', 'email', 'totalinvestment']

    def get_totalinvestment(self, obj):
        return Investment.objects.filter(owner=obj.id).count()
        # return GallerySerializer(logger_queryset, many=True).data


class PeriodInvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = ['id', 'period', ]


class RiskRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Risk
        fields = ['id', 'risk', ]


class DealTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = DealType
        fields = ['id', 'name', 'is_active', ]


class CurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = ['id', 'name', 'is_active', ]


class MainRoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = MainRoom
        fields = ['id', 'slug', 'name', 'description',
                  'is_verified', ]


class CreateRoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = InvestmentRoom
        fields = ['id', 'main_room', 'slug', 'name', 'description',
                  'is_verified', ]


class RoomSerializer(serializers.ModelSerializer):
    main_room = MainRoomSerializer(many=False, read_only=False)

    class Meta:
        model = InvestmentRoom
        fields = ['id', 'main_room', 'slug', 'name', 'description',
                  'is_verified', ]

    def get_main_room(self, instance):
        return instance.geo_info.main_room


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


class GalleryUDSerializer(serializers.ModelSerializer):
    gallery_url = serializers.SerializerMethodField("get_image_url")
    # gallery = serializers.ImageField(
    # max_length=None, allow_empty_file=False, allow_null=False, use_url=True, required=False)

    class Meta:
        model = Gallery
        fields = ['id', 'gallery',  'is_featured']

    def get_image_url(self, obj):
        return obj.gallery.url

    '''
    def get_gallery(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.gallery.url)
        '''


class GalleryUpdateSerializer(serializers.ModelSerializer):
    # gallery_url = serializers.SerializerMethodField("get_image_url")
    # gallery = serializers.ImageField(
    # max_length=None, allow_empty_file=False, allow_null=False, use_url=True, required=False)

    class Meta:
        model = Gallery
        fields = ['id', 'gallery',  'is_featured']

    '''
    def get_image_url(self, obj):
        return obj.gallery.url


    def get_gallery(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.gallery.url)
        '''


class InvestmentRoomSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    amountAlloted = serializers.SerializerMethodField()
    balanceToBeAlloted = serializers.SerializerMethodField()
    currency = CurrencySerializer(many=False, read_only=False)
    dealtype = DealTypeSerializer(many=False, read_only=False)
    # gallery_set = serializers.StringRelatedField(many=True)
    risk = RiskRoomSerializer(many=False, read_only=False)
    room = RoomSerializer(many=False, read_only=False)
    period = PeriodInvestmentSerializer(read_only=False)
    owner = UserInvestmentSerializer(read_only=False)
    # gallery_investment = GallerySerializer(read_only=False)

    '''
    def get_image(self, gallery):
        pesticide_qs = Gallery.objects.filter(
            gallery__investment=gallery)
        return Gall erySerializer(pesticide_qs, many=True).data
        '''

    class Meta:
        model = Investment
        fields = ['id', 'owner', 'slug', 'name', 'description', 'currency', 'amount',
                  'volume', 'project_raise', 'project_cost', 'periodic_payment', 'milestone', 'minimum_allotment', 'maximum_allotment', 'offer_price',
                  'amountAlloted', 'balanceToBeAlloted', 'spot_price', 'unit_price', 'dealtype', 'location', 'video', 'room', 'roi', 'period',
                  'annualized',  'risk', 'features', 'is_verified', 'image', 'start_date', 'end_date', 'created_at']

    def get_image(self, obj):
        logger_queryset = Gallery.objects.filter(investment=obj.id)
        return GallerySerializer(logger_queryset, many=True).data

    def get_amountAlloted(self, obj):
        return Investors.objects.filter(investment=obj.id, is_approved=True).aggregate(Sum('amount'))

    def get_balanceToBeAlloted(self, obj):
        totalamount = Investors.objects.filter(
            investment=obj.id, is_approved=True).aggregate(Sum('amount'))
        print(obj.project_raise)
        print(totalamount)
        print(totalamount.get('amount__sum'))
        if totalamount.get('amount__sum') is None:
            amount = 0
        else:
            amount = totalamount.get('amount__sum')
        totalBalance = int(obj.project_raise) - amount
        return totalBalance

    '''
    def get_image_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.image_url)
        '''

    def get_room(self, instance):
        return instance.geo_info.room

    def get_risk(self, instance):
        return instance.geo_info.risk

    def get_owner(self, instance):
        return instance.geo_info.owner

    def get_userdetails(self, instance):
        return instance.geo_info.userdetails


class InvestmentSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    amountAlloted = serializers.SerializerMethodField()
    balanceToBeAlloted = serializers.SerializerMethodField()
    currency = CurrencySerializer(many=False, read_only=False)
    dealtype = DealTypeSerializer(many=False, read_only=False)
    # gallery_set = serializers.StringRelatedField(many=True)
    risk = RiskRoomSerializer(many=False, read_only=False)
    room = RoomSerializer(many=False, read_only=False)
    period = PeriodInvestmentSerializer(read_only=False)
    owner = UserInvestmentSerializer(read_only=False)
    investorsCount = serializers.SerializerMethodField()
    # gallery_investment = GallerySerializer(read_only=False)

    '''
    def get_image(self, gallery):
        pesticide_qs = Gallery.objects.filter(
            gallery__investment=gallery)
        return GallerySerializer(pesticide_qs, many=True).data
        '''

    class Meta:
        model = Investment
        fields = ['id', 'owner', 'slug', 'name', 'description', 'currency', 'amount',
                  'volume', 'project_raise', 'project_cost', 'periodic_payment', 'milestone', 'minimum_allotment', 'maximum_allotment', 'offer_price',
                  'amountAlloted', 'balanceToBeAlloted', 'spot_price', 'unit_price', 'dealtype', 'location', 'video', 'room', 'roi', 'period',
                  'annualized',  'risk', 'features', 'is_verified', 'image', 'start_date', 'end_date', 'created_at', 'investorsCount']

    def get_image(self, obj):
        logger_queryset = Gallery.objects.filter(
            investment=obj.id).order_by('-is_featured')
        return GallerySerializer(logger_queryset, many=True).data

    def get_investorsCount(self, obj):
        in_queryset = Investors.objects.filter(investment=obj.id).count()
        return in_queryset

    def get_amountAlloted(self, obj):
        return Investors.objects.filter(investment=int(obj.id), is_approved=True).aggregate(Sum('amount'))

    def get_balanceToBeAlloted(self, obj):
        totalamount = Investors.objects.filter(
            investment=int(obj.id), is_approved=True).aggregate(Sum('amount'))

        if totalamount.get('amount__sum') is None:

            totalBalance = int(obj.project_raise) - 0
        else:
            totalBalance = int(obj.project_raise) - \
                int(totalamount.get('amount__sum'))

        return totalBalance

    '''
    def get_image_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.image_url)
        '''

    def get_room(self, instance):
        return instance.geo_info.room

    def get_risk(self, instance):
        return instance.geo_info.risk

    def get_owner(self, instance):
        return instance.geo_info.owner

    def get_userdetails(self, instance):
        return instance.geo_info.userdetails


class TotalInvestmentSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField()
    # amount = serializers.SerializerMethodField()

    class Meta:
        model = Investment
        fields = ['amount']

    '''
    def get_amount(self, obj):
        queryset = Investment.objects.aggregate(Sum(obj.amount))
        return queryset'''


class InvestmentOnlySerializer(serializers.ModelSerializer):

    class Meta:
        model = Investment
        fields = ['id', 'owner', 'slug', 'name', 'description', 'currency', 'amount',
                  'project_cost', 'project_raise', 'periodic_payment', 'milestone', 'minimum_allotment', 'maximum_allotment',
                  'volume', 'offer_price', 'spot_price', 'unit_price', 'dealtype', 'location', 'video', 'room', 'roi', 'period',
                  'annualized',  'risk', 'is_closed', 'features', 'is_verified', 'start_date', 'end_date', 'created_at']


class ApproveInvestmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Investment
        fields = ['id', 'is_verified']


class CloseInvestmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Investment
        fields = ['id', 'is_closed']


class InvestorsSerializer(serializers.ModelSerializer):

    class Meta:
        model = InvestmentRoom
        fields = ['investment', 'id', 'investor', 'is_closed', 'bid_price',
                  'is_approved', 'amount', 'serialkey', 'approved_by',
                  'is_closed', 'closed_by', 'created_at']
