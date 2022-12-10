from rest_framework import serializers
from investment.models import Investment, InvestmentRoom, Gallery, Investors
from investor.models import Period, Risk
from authentication.models import User
from django.conf import settings
from django.db.models import Sum, Aggregate, Avg
from .models import Comment


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'firstname', 'lastname', 'email']


class InvestorSerializer(serializers.ModelSerializer):
    investor = UserSerializer(many=False, read_only=False)

    class Meta:
        model = Investors
        fields = ['id', 'investor']


class AdminCommentSerializer(serializers.ModelSerializer):
    #investor = UserSerializer(many=False, read_only=False)

    class Meta:
        model = Comment
        fields = ['id', 'slug', 'comment', 'investor',
                  'is_closed', 'responded_by', 'created_at']


class AdminDetailCommentSerializer(serializers.ModelSerializer):
    responded_by = UserSerializer(many=False, read_only=False)

    class Meta:
        model = Comment
        fields = ['id', 'comment', 'investor',
                  'is_closed', 'responded_by', 'created_at']

    def get_responded_by(self, instance):
        return instance.geo_info.responded_by


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'slug', 'comment', 'investor',
                  'is_closed', 'created_at']


class ListCommentSerializer(serializers.ModelSerializer):
    investor = InvestorSerializer(many=False, read_only=False)
    responded_by = UserSerializer(many=False, read_only=False)

    class Meta:
        model = Comment
        fields = ['id', 'slug', 'responded_by',
                  'comment', 'investor', 'is_closed']


class UserInvestorsSerializer(serializers.ModelSerializer):
    totalcomments = serializers.SerializerMethodField()
    investor = UserSerializer(many=False, read_only=False)

    class Meta:
        model = Investors
        fields = ['id', 'investor', 'amount',
                  'serialkey', 'totalcomments', 'created_at']

    def get_totalcomments(self, obj):
        return Comment.objects.filter(investor=obj.id).count()

    def get_investor(self, instance):
        return instance.geo_info.investor


class DetailInvestorSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    investor = UserSerializer(many=False, read_only=False)

    class Meta:
        model = Investors
        fields = ['id', 'investor', 'amount',
                  'serialkey', 'comments', 'created_at']

    def get_comments(self, obj):
        logger_request = Comment.objects.filter(investor=obj.id)
        return AdminDetailCommentSerializer(logger_request, many=True).data

    def get_investor(self, instance):
        return instance.geo_info.investor
