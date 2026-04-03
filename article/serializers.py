import re
import bleach
from rest_framework import serializers
from .models import Article, ArticleCategory, MediaFile, ArticleStatus

SLUG_REGEX = r"^[a-z0-9]+(?:-[a-z0-9]+)*$"

ALLOWED_TAGS = [
    "p", "br", "strong", "em", "u", "ul", "ol", "li",
    "a", "blockquote", "h1", "h2", "h3", "h4", "h5", "h6",
    "img"
]

ALLOWED_ATTRIBUTES = {
    "a": ["href", "title", "target", "rel"],
    "img": ["src", "alt", "title"]
}


class ArticleCategorySerializer(serializers.ModelSerializer):
    article_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = ArticleCategory
        fields = ["id", "name", "slug", "description", "article_count"]

    def validate_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Name must be at least 2 characters.")
        return value.strip()

    def validate_slug(self, value):
        if value and not re.match(SLUG_REGEX, value):
            raise serializers.ValidationError("Slug must be URL-friendly.")

        qs = ArticleCategory.objects.filter(slug=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if value and qs.exists():
            raise serializers.ValidationError("Category slug already exists.")
        return value


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    date = serializers.DateTimeField(source="created_at", read_only=True)
    featured_media = serializers.SerializerMethodField()
    og_image = serializers.SerializerMethodField()
    featured_image_url = serializers.SerializerMethodField()
    category = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=ArticleCategory.objects.all()
    )
    category_detail = ArticleCategorySerializer(source="category", read_only=True)
    categories = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            "id",
            "slug",
            "title",
            "content",
            "excerpt",
            "category",
            "category_detail",
            "tags",
            "featured_media",
            "featured_media_type",
            "status",
            "featured",
            "meta_title",
            "meta_description",
            "og_image",
            "author",
            "date",
            "link",
            "categories",
            "featured_image_url",
        ]

    def get_author(self, obj):
        full_name = getattr(obj.author, "get_full_name", lambda: "")()
        return full_name.strip() or getattr(obj.author, "username", str(obj.author))

    def get_featured_media(self, obj):
        request = self.context.get("request")
        if obj.featured_media:
            return request.build_absolute_uri(obj.featured_media.url) if request else obj.featured_media.url
        return None

    def get_og_image(self, obj):
        request = self.context.get("request")
        if obj.og_image:
            return request.build_absolute_uri(obj.og_image.url) if request else obj.og_image.url
        return None

    def get_featured_image_url(self, obj):
        request = self.context.get("request")
        if obj.featured_media:
            return request.build_absolute_uri(obj.featured_media.url) if request else obj.featured_media.url
        return None

    def get_categories(self, obj):
        return [obj.category.id] if obj.category else []

    def validate_title(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters.")
        return value.strip()

    def validate_slug(self, value):
        if value and not re.match(SLUG_REGEX, value):
            raise serializers.ValidationError("Slug must be URL-friendly.")

        qs = Article.objects.filter(slug=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if value and qs.exists():
            raise serializers.ValidationError("Article slug already exists.")
        return value

    def validate_content(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Content must be at least 10 characters.")
        if len(value) > 100000:
            raise serializers.ValidationError("Content must not exceed 100,000 characters.")

        cleaned = bleach.clean(
            value,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=True
        )
        return cleaned

    def validate_excerpt(self, value):
        if value and len(value) > 500:
            raise serializers.ValidationError("Excerpt must not exceed 500 characters.")
        return value

    def validate_meta_title(self, value):
        if value and len(value) > 60:
            raise serializers.ValidationError("Meta title must not exceed 60 characters.")
        return value

    def validate_meta_description(self, value):
        if value and len(value) > 160:
            raise serializers.ValidationError("Meta description must not exceed 160 characters.")
        return value

    def validate_status(self, value):
        valid = [choice[0] for choice in ArticleStatus.choices]
        if value not in valid:
            raise serializers.ValidationError("Invalid status value.")
        return value

    def validate_tags(self, value):
        if isinstance(value, str):
            tags = [tag.strip() for tag in value.split(",") if tag.strip()]
        elif isinstance(value, list):
            tags = [str(tag).strip() for tag in value if str(tag).strip()]
        else:
            raise serializers.ValidationError("Tags must be a comma-separated string or list.")

        if len(tags) > 10:
            raise serializers.ValidationError("Maximum of 10 tags allowed.")

        for tag in tags:
            if len(tag) > 50:
                raise serializers.ValidationError(f"Tag '{tag}' exceeds 50 characters.")

        return tags


class ArticleCreateUpdateSerializer(ArticleSerializer):
    class Meta(ArticleSerializer.Meta):
        fields = [
            "title",
            "slug",
            "content",
            "excerpt",
            "category",
            "tags",
            "featured_media",
            "featured_media_type",
            "status",
            "featured",
            "meta_title",
            "meta_description",
            "og_image",
            "link",
        ]


class MediaUploadSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    directory = serializers.SerializerMethodField()
    filename = serializers.SerializerMethodField()

    class Meta:
        model = MediaFile
        fields = [
            "id",
            "directory",
            "filename",
            "url",
            "size",
            "mime_type",
            "type",
        ]

    def get_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.file.url) if request else obj.file.url

    def get_directory(self, obj):
        import os
        return os.path.dirname(obj.file.url)

    def get_filename(self, obj):
        import os
        return os.path.basename(obj.file.name)