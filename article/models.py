from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.core.exceptions import ValidationError
import re


SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class ArticleCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Article Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def clean(self):
        if self.slug and not SLUG_PATTERN.match(self.slug):
            raise ValidationError({
                "slug": "Slug must be lowercase, alphanumeric and hyphen-separated only."
            })

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)[:100]
            slug = base_slug
            counter = 1
            while ArticleCategory.objects.exclude(pk=self.pk).filter(slug=slug).exists():
                suffix = f"-{counter}"
                slug = f"{base_slug[:100 - len(suffix)]}{suffix}"
                counter += 1
            self.slug = slug

        self.full_clean()
        super().save(*args, **kwargs)


class ArticleStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    PENDING = "pending", "Pending"
    APPROVED = "approved", "Approved"
    PUBLISHED = "published", "Published"
    ARCHIVED = "archived", "Archived"


class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = models.TextField()
    excerpt = models.CharField(max_length=500, blank=True, null=True)

    category = models.ForeignKey(
        ArticleCategory,
        on_delete=models.PROTECT,
        related_name="articles",
        null=True,
        blank=True,
    )

    tags = models.JSONField(default=list, blank=True)

    featured_media = models.ImageField(
        upload_to="uploads/featured/%Y/%m/%d/",
        blank=True,
        null=True
    )
    featured_media_type = models.CharField(
        max_length=20,
        choices=[("local", "Local"), ("external", "External")],
        default="local"
    )

    status = models.CharField(
        max_length=20,
        choices=ArticleStatus.choices,
        default=ArticleStatus.DRAFT
    )
    featured = models.BooleanField(default=False)

    meta_title = models.CharField(max_length=60, blank=True, null=True)
    meta_description = models.CharField(max_length=160, blank=True, null=True)
    og_image = models.ImageField(
        upload_to="uploads/og/%Y/%m/%d/",
        blank=True,
        null=True
    )

    link = models.URLField(blank=True, null=True)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="articles"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def clean(self):
        if self.slug and not SLUG_PATTERN.match(self.slug):
            raise ValidationError({
                "slug": "Slug must be lowercase, alphanumeric and hyphen-separated only."
            })

        if self.title and len(self.title.strip()) < 3:
            raise ValidationError({
                "title": "Title must be at least 3 characters."
            })

        if self.content and len(self.content.strip()) < 10:
            raise ValidationError({
                "content": "Content must be at least 10 characters."
            })

        if self.excerpt and len(self.excerpt) > 500:
            raise ValidationError({
                "excerpt": "Excerpt must not exceed 500 characters."
            })

        if self.meta_title and len(self.meta_title) > 60:
            raise ValidationError({
                "meta_title": "Meta title must not exceed 60 characters."
            })

        if self.meta_description and len(self.meta_description) > 160:
            raise ValidationError({
                "meta_description": "Meta description must not exceed 160 characters."
            })

        if self.tags:
            if len(self.tags) > 10:
                raise ValidationError({
                    "tags": "Maximum of 10 tags allowed."
                })

            for tag in self.tags:
                if len(tag) > 50:
                    raise ValidationError({
                        "tags": f"Tag '{tag}' exceeds 50 characters."
                    })

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)[:200]
            slug = base_slug
            counter = 1
            while Article.objects.exclude(pk=self.pk).filter(slug=slug).exists():
                suffix = f"-{counter}"
                slug = f"{base_slug[:200 - len(suffix)]}{suffix}"
                counter += 1
            self.slug = slug

        self.full_clean()
        super().save(*args, **kwargs)


class MediaFile(models.Model):
    MEDIA_TYPE_CHOICES = [
        ("featured", "Featured"),
        ("attachment", "Attachment"),
    ]

    file = models.FileField(upload_to="uploads/%Y/%m/%d/")
    original_name = models.CharField(max_length=255)
    mime_type = models.CharField(max_length=100)
    size = models.PositiveIntegerField()
    type = models.CharField(max_length=20, choices=MEDIA_TYPE_CHOICES)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.original_name