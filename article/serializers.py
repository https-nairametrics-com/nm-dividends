from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'slug', 'content', 'author', 'created_at', 'updated_at', 'featured_image']
        extra_kwargs = {
            'content': {'required': True},  # Ensure content is required (it will accept HTML)
        }

    def to_representation(self, instance):
        """
        Custom method to ensure content is rendered with HTML tags.
        """
        representation = super().to_representation(instance)
        representation['content'] = instance.content  # Ensure the HTML content is passed as-is
        return representation

class PostArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['title', 'slug', 'content', 'featured_image']
        extra_kwargs = {
            'content': {'required': True},  # Ensure content is required (it will accept HTML)
        }

    def to_representation(self, instance):
        """
        Custom method to ensure content is rendered with HTML tags.
        """
        representation = super().to_representation(instance)
        representation['content'] = instance.content  # Ensure the HTML content is passed as-is
        return representation
