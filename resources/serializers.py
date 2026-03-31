"""
Serializers for the resources app.
"""

from rest_framework import serializers
from .models import Resource, MediaFile, ResourceCategory, ResourceStatus


class ResourceSerializer(serializers.ModelSerializer):
    """Serializer for Resource model."""
    
    author = serializers.SerializerMethodField(read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Resource
        fields = [
            'id',
            'slug',
            'title',
            'content',
            'excerpt',
            'category',
            'category_display',
            'tags',
            'featured_media',
            'featured_media_type',
            'status',
            'status_display',
            'featured',
            'meta_title',
            'meta_description',
            'og_image',
            'author',
            'author_name',
            'author_user',
            'date',
            'link',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at', 'author']
        extra_kwargs = {
            'author_user': {'write_only': True, 'required': False},
        }
    
    def get_author(self, obj):
        """Return author display name."""
        return obj.author
    
    def validate_tags(self, value):
        """Validate that tags list does not exceed 10 items."""
        if isinstance(value, list) and len(value) > 10:
            raise serializers.ValidationError("Maximum 10 tags allowed.")
        return value
    
    def validate_status(self, value):
        """Validate status transitions (optional enhancement)."""
        return value


class ResourceCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating resources.
    
    Allows setting slug manually or auto-generating from title.
    """
    
    author = serializers.SerializerMethodField(read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Resource
        fields = [
            'id',
            'slug',
            'title',
            'content',
            'excerpt',
            'category',
            'category_display',
            'tags',
            'featured_media',
            'featured_media_type',
            'status',
            'status_display',
            'featured',
            'meta_title',
            'meta_description',
            'og_image',
            'author',
            'author_name',
            'author_user',
            'date',
            'link',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'author']
    
    def get_author(self, obj):
        """Return author display name."""
        return obj.author
    
    def validate_tags(self, value):
        """Validate that tags list does not exceed 10 items."""
        if isinstance(value, list) and len(value) > 10:
            raise serializers.ValidationError("Maximum 10 tags allowed.")
        return value


class MediaFileSerializer(serializers.ModelSerializer):
    """Serializer for MediaFile model."""
    
    url = serializers.SerializerMethodField(read_only=True)
    uploaded_by_username = serializers.CharField(source='uploaded_by.username', read_only=True)
    
    class Meta:
        model = MediaFile
        fields = [
            'id',
            'file',
            'url',
            'original_filename',
            'file_type',
            'file_size',
            'uploaded_by',
            'uploaded_by_username',
            'uploaded_at',
            'resource',
        ]
        read_only_fields = ['id', 'url', 'original_filename', 'file_type', 'file_size', 'uploaded_by_username', 'uploaded_at']
        extra_kwargs = {
            'uploaded_by': {'write_only': True, 'required': False},
            'resource': {'required': False},
        }
    
    def get_url(self, obj):
        """Return the file URL."""
        if obj.file:
            return obj.file.url
        return None


class ResourceListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for resource list views.
    
    Excludes full content to reduce payload size.
    """
    
    author = serializers.SerializerMethodField(read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Resource
        fields = [
            'id',
            'slug',
            'title',
            'excerpt',
            'category',
            'category_display',
            'tags',
            'featured_media',
            'featured_media_type',
            'status',
            'status_display',
            'featured',
            'meta_title',
            'meta_description',
            'author',
            'date',
            'created_at',
            'updated_at',
        ]
    
    def get_author(self, obj):
        """Return author display name."""
        return obj.author


class CategoryCountSerializer(serializers.Serializer):
    """Serializer for category counts endpoint."""
    
    category = serializers.CharField()
    display_name = serializers.CharField()
    count = serializers.IntegerField()
