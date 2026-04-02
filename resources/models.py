"""
Resources app models for content management.

This module defines the database models for the Resources API, including
articles, disclosures, news, and actions with SEO optimization fields,
status workflows, and media tracking.
"""

import os
import uuid
from django.db import models
from django.contrib.postgres.indexes import GinIndex
from django.utils.text import slugify
from django.utils import timezone


class ResourceCategory(models.TextChoices):
    """Categories for resources."""

    ARTICLE = "article", "Article"
    DISCLOSURE = "disclosure", "Disclosure"
    NEWS = "news", "News"
    ACTIONS = "actions", "Actions"


class ResourceStatus(models.TextChoices):
    """Status workflow for resources."""

    DRAFT = "draft", "Draft"
    PENDING = "pending", "Pending"
    APPROVED = "approved", "Approved"
    PUBLISHED = "published", "Published"
    ARCHIVED = "archived", "Archived"


class MediaType(models.TextChoices):
    """Types of featured media."""

    LOCAL = "local", "Local"
    EXTERNAL = "external", "External"


class Resource(models.Model):
    """
    Resource model for content management.

    Supports articles, disclosures, news, and actions with full
    SEO optimization, status workflow, and tagging capabilities.
    """

    # Primary identification
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        help_text="URL-friendly identifier (auto-generated from title if blank)",
    )
    title = models.CharField(max_length=255, help_text="Resource title")

    # Content fields
    content = models.TextField(help_text="Rich HTML content")
    excerpt = models.TextField(blank=True, help_text="Short description or summary")

    # Categorization
    category = models.CharField(
        max_length=20,
        choices=ResourceCategory.choices,
        default=ResourceCategory.ARTICLE,
        help_text="Resource category",
    )
    tags = models.JSONField(
        default=list, blank=True, help_text="List of tags (maximum 10)"
    )

    # Media
    featured_media = models.CharField(
        max_length=500, blank=True, help_text="URL to featured image or media"
    )
    featured_media_type = models.CharField(
        max_length=10,
        choices=MediaType.choices,
        default=MediaType.LOCAL,
        blank=True,
        help_text="Type of featured media",
    )

    # Status and workflow
    status = models.CharField(
        max_length=20,
        choices=ResourceStatus.choices,
        default=ResourceStatus.DRAFT,
        help_text="Publication status",
    )
    featured = models.BooleanField(
        default=False, help_text="Whether this resource is featured"
    )

    # SEO fields
    meta_title = models.CharField(
        max_length=255,
        blank=True,
        help_text="SEO title (if different from resource title)",
    )
    meta_description = models.TextField(blank=True, help_text="SEO meta description")
    og_image = models.CharField(
        max_length=500, blank=True, help_text="Open Graph image URL for social sharing"
    )

    # Author information
    author_name = models.CharField(
        max_length=255, blank=True, help_text="Author display name"
    )
    author_user = models.ForeignKey(
        "authentication.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="resources",
        help_text="Author user account (if applicable)",
    )

    # Publication
    date = models.DateTimeField(default=timezone.now, help_text="Publication date")
    link = models.URLField(
        blank=True,
        null=True,
        help_text="External link (if resource links to external content)",
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta options for Resource model."""

        ordering = ["-created_at"]
        indexes = [
            # Basic field indexes
            models.Index(fields=["category"]),
            models.Index(fields=["status"]),
            models.Index(fields=["date"]),
            models.Index(fields=["featured"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["updated_at"]),
            # Composite indexes for common queries
            models.Index(fields=["status", "category"]),
            models.Index(fields=["status", "featured"]),
            models.Index(fields=["status", "category", "featured"]),
            # GIN index for full-text search on title and content
            GinIndex(
                name="resource_title_gin_idx",
                fields=["title"],
                opclasses=["gin_trgm_ops"],
            ),
        ]
        verbose_name = "Resource"
        verbose_name_plural = "Resources"

    def __str__(self):
        """Return string representation."""
        return self.title

    def clean(self):
        """Validate model fields."""
        from django.core.exceptions import ValidationError

        # Validate tag count (max 10)
        if isinstance(self.tags, list) and len(self.tags) > 10:
            raise ValidationError({"tags": "Maximum 10 tags allowed."})

        # Ensure tags is a list
        if self.tags is None:
            self.tags = []

    def save(self, *args, **kwargs):
        """
        Save the resource with auto-generated slug if not provided.

        Auto-generates a unique slug from the title if not provided.
        Handles duplicate slugs by appending a counter.
        """
        # Validate before saving
        self.clean()

        # Auto-generate slug if not provided
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1

            # Ensure unique slug
            while Resource.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    @property
    def author(self):
        """
        Return author display name.

        Returns author_name if set, otherwise falls back to author_user's info.
        """
        if self.author_name:
            return self.author_name
        if self.author_user:
            return self.author_user.username or self.author_user.email
        return "Anonymous"

    @property
    def tag_list(self):
        """Return tags as a list."""
        if isinstance(self.tags, list):
            return self.tags
        return []


def media_file_path(instance, filename):
    """
    Generate file path for uploaded media files.

    Organizes files by user ID and date to prevent conflicts
    and maintain a clean directory structure.
    """
    # Extract file extension
    ext = filename.split(".")[-1] if "." in filename else ""

    # Generate unique filename
    unique_filename = f"{uuid.uuid4().hex}.{ext}" if ext else uuid.uuid4().hex

    # Build path: media/uploads/{user_id}/{year}/{month}/{filename}
    user_id = instance.uploaded_by_id or "anonymous"
    now = timezone.now()

    return os.path.join(
        "uploads", str(user_id), str(now.year), str(now.month).zfill(2), unique_filename
    )


class MediaFile(models.Model):
    """
    Model for tracking uploaded media files.

    Stores metadata about uploaded files including the original
    filename, file type, and upload information.
    """

    # File storage
    file = models.FileField(upload_to=media_file_path, help_text="Uploaded file")
    original_filename = models.CharField(
        max_length=255, help_text="Original filename before renaming"
    )
    file_type = models.CharField(
        max_length=50, blank=True, help_text="MIME type or file extension"
    )
    file_size = models.PositiveIntegerField(
        null=True, blank=True, help_text="File size in bytes"
    )

    # Upload tracking
    uploaded_by = models.ForeignKey(
        "authentication.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="media_files",
        help_text="User who uploaded the file",
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    # Optional link to resource
    resource = models.ForeignKey(
        Resource,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="media_files",
        help_text="Associated resource (if any)",
    )

    class Meta:
        """Meta options for MediaFile model."""

        ordering = ["-uploaded_at"]
        indexes = [
            models.Index(fields=["uploaded_by"]),
            models.Index(fields=["uploaded_at"]),
            models.Index(fields=["resource"]),
            models.Index(fields=["file_type"]),
        ]
        verbose_name = "Media File"
        verbose_name_plural = "Media Files"

    def __str__(self):
        """Return string representation."""
        return self.original_filename or f"Media {self.pk}"

    def save(self, *args, **kwargs):
        """Save the media file with metadata extraction."""
        # Store original filename if not set
        if not self.original_filename and self.file:
            self.original_filename = self.file.name

        # Extract file type from filename
        if not self.file_type and self.original_filename:
            ext = (
                self.original_filename.split(".")[-1].lower()
                if "." in self.original_filename
                else ""
            )
            self.file_type = ext

        # Get file size
        if self.file and hasattr(self.file, "size"):
            self.file_size = self.file.size

        super().save(*args, **kwargs)

    @property
    def url(self):
        """Return the file URL."""
        if self.file:
            return self.file.url
        return None

    def delete(self, *args, **kwargs):
        """Delete the file from storage when model instance is deleted."""
        # Store file path before deletion
        file_path = self.file.path if self.file else None

        # Delete the model instance
        super().delete(*args, **kwargs)

        # Delete the actual file from storage
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except OSError:
                pass  # File may already be deleted or inaccessible
