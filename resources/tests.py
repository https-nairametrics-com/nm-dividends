"""
Test suite for the resources app.

This module contains comprehensive tests for the Resources API including:
- CRUD operations
- Permissions
- Filters and search
- Pagination
- Media uploads
"""

import os
import tempfile
from io import BytesIO

import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from resources.models import Resource, MediaFile, ResourceCategory, ResourceStatus


User = get_user_model()


@pytest.fixture
def api_client():
    """Return an API client for testing."""
    return APIClient()


@pytest.fixture
def regular_user(db):
    """Create a regular user."""
    return User.objects.create_user(
        email="user@example.com",
        username="regularuser",
        password="testpass123",
        firstname="Regular",
        lastname="User",
        referral_code="REG001",
    )


@pytest.fixture
def admin_user(db):
    """Create an admin/staff user."""
    user = User.objects.create_user(
        email="admin@example.com",
        username="adminuser",
        password="testpass123",
        firstname="Admin",
        lastname="User",
        referral_code="ADM001",
    )
    user.is_staff = True
    user.is_superuser = True
    user.save()
    return user


@pytest.fixture
def sample_resource(admin_user):
    """Create a sample published resource."""
    return Resource.objects.create(
        title="Test Article",
        content="This is test content",
        excerpt="Test excerpt",
        category=ResourceCategory.ARTICLE,
        status=ResourceStatus.PUBLISHED,
        author_user=admin_user,
        author_name="Test Author",
    )


@pytest.fixture
def draft_resource(admin_user):
    """Create a draft resource."""
    return Resource.objects.create(
        title="Draft Article",
        content="Draft content",
        category=ResourceCategory.NEWS,
        status=ResourceStatus.DRAFT,
        author_user=admin_user,
    )


@pytest.fixture
def sample_media_file(admin_user):
    """Create a sample media file."""
    # Create a temporary image file
    image_data = BytesIO(b"fake image data")
    image_file = SimpleUploadedFile(
        "test_image.jpg", image_data.read(), content_type="image/jpeg"
    )

    return MediaFile.objects.create(
        file=image_file,
        original_filename="test_image.jpg",
        file_type="jpg",
        uploaded_by=admin_user,
    )


class TestResourceListAPI:
    """Test the resources list endpoint."""

    def test_list_resources_public(self, api_client, sample_resource):
        """Test that public users can list published resources."""
        url = reverse("resource-list")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True
        assert len(response.data["data"]) == 1
        assert response.data["meta"]["total"] == 1

    def test_list_resources_no_drafts_for_public(self, api_client, draft_resource):
        """Test that draft resources are not shown to public users."""
        url = reverse("resource-list")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["data"]) == 0

    def test_list_resources_staff_sees_all(
        self, api_client, admin_user, draft_resource
    ):
        """Test that staff users can see all resources including drafts."""
        api_client.force_authenticate(user=admin_user)
        url = reverse("resource-list")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["data"]) == 1

    def test_list_resources_pagination(self, api_client, admin_user):
        """Test pagination works correctly."""
        # Create multiple resources
        for i in range(15):
            Resource.objects.create(
                title=f"Resource {i}",
                content=f"Content {i}",
                status=ResourceStatus.PUBLISHED,
            )

        url = reverse("resource-list")
        response = api_client.get(url, {"page": 1, "per_page": 10})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["data"]) == 10
        assert response.data["meta"]["total"] == 15
        assert response.data["meta"]["total_pages"] == 2

    def test_list_resources_max_page_size(self, api_client, admin_user):
        """Test that per_page is capped at 100."""
        url = reverse("resource-list")
        response = api_client.get(url, {"per_page": 200})

        assert response.status_code == status.HTTP_200_OK
        assert response.data["meta"]["per_page"] <= 100


class TestResourceCreateAPI:
    """Test the resource create endpoint."""

    def test_create_resource_admin(self, api_client, admin_user):
        """Test that admin users can create resources."""
        api_client.force_authenticate(user=admin_user)
        url = reverse("resource-list")
        data = {
            "title": "New Article",
            "content": "New content",
            "category": ResourceCategory.ARTICLE,
            "status": ResourceStatus.PUBLISHED,
        }
        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["success"] is True
        assert response.data["data"]["title"] == "New Article"
        assert Resource.objects.count() == 1

    def test_create_resource_public_unauthorized(self, api_client):
        """Test that public users cannot create resources."""
        url = reverse("resource-list")
        data = {
            "title": "New Article",
            "content": "New content",
            "category": ResourceCategory.ARTICLE,
        }
        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_resource_regular_user_forbidden(self, api_client, regular_user):
        """Test that regular users cannot create resources."""
        api_client.force_authenticate(user=regular_user)
        url = reverse("resource-list")
        data = {"title": "New Article", "content": "New content"}
        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_resource_regular_user_forbidden(self, api_client, regular_user):
        """Test that regular users cannot create resources."""
        api_client.force_authenticate(user=regular_user)
        url = reverse("resource-list")
        data = {"title": "New Article", "content": "New content"}
        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_resource_auto_slug(self, api_client, admin_user):
        """Test that slug is auto-generated from title."""
        api_client.force_authenticate(user=admin_user)
        url = reverse("resource-list")
        data = {
            "title": "My Test Article",
            "content": "Content",
            "category": ResourceCategory.ARTICLE,
        }
        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["data"]["slug"] == "my-test-article"


class TestResourceRetrieveAPI:
    """Test the resource retrieve endpoint."""

    def test_retrieve_published_resource_public(self, api_client, sample_resource):
        """Test that public users can retrieve published resources."""
        url = reverse("resource-detail", kwargs={"slug": sample_resource.slug})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True
        assert response.data["data"]["title"] == sample_resource.title

    def test_retrieve_draft_resource_public_forbidden(self, api_client, draft_resource):
        """Test that public users cannot retrieve draft resources."""
        url = reverse("resource-detail", kwargs={"slug": draft_resource.slug})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_retrieve_draft_resource_staff_allowed(
        self, api_client, admin_user, draft_resource
    ):
        """Test that staff users can retrieve draft resources."""
        api_client.force_authenticate(user=admin_user)
        url = reverse("resource-detail", kwargs={"slug": draft_resource.slug})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"]["title"] == draft_resource.title


class TestResourceUpdateAPI:
    """Test the resource update endpoint."""

    def test_update_resource_admin(self, api_client, admin_user, sample_resource):
        """Test that admin users can update resources."""
        api_client.force_authenticate(user=admin_user)
        url = reverse("resource-detail", kwargs={"slug": sample_resource.slug})
        data = {
            "title": "Updated Title",
            "content": "Updated content",
            "category": ResourceCategory.ARTICLE,
        }
        response = api_client.put(url, data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True
        assert response.data["data"]["title"] == "Updated Title"

    def test_partial_update_resource(self, api_client, admin_user, sample_resource):
        """Test partial update works correctly."""
        api_client.force_authenticate(user=admin_user)
        url = reverse("resource-detail", kwargs={"slug": sample_resource.slug})
        data = {"title": "Partially Updated Title"}
        response = api_client.patch(url, data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"]["title"] == "Partially Updated Title"
        # Content should remain unchanged
        assert response.data["data"]["content"] == sample_resource.content


class TestResourceDeleteAPI:
    """Test the resource delete endpoint."""

    def test_delete_resource_admin(self, api_client, admin_user, sample_resource):
        """Test that admin users can delete resources."""
        api_client.force_authenticate(user=admin_user)
        url = reverse("resource-detail", kwargs={"slug": sample_resource.slug})
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True
        assert Resource.objects.count() == 0

    def test_delete_resource_public_unauthorized(self, api_client, sample_resource):
        """Test that public users cannot delete resources."""
        url = reverse("resource-detail", kwargs={"slug": sample_resource.slug})
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestResourceFilters:
    """Test resource filtering functionality."""

    def test_filter_by_category(self, api_client, admin_user):
        """Test filtering by category."""
        Resource.objects.create(
            title="Article 1",
            content="Content",
            category=ResourceCategory.ARTICLE,
            status=ResourceStatus.PUBLISHED,
        )
        Resource.objects.create(
            title="News 1",
            content="Content",
            category=ResourceCategory.NEWS,
            status=ResourceStatus.PUBLISHED,
        )

        url = reverse("resource-list")
        response = api_client.get(url, {"category": ResourceCategory.ARTICLE})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["data"]) == 1
        assert response.data["data"][0]["category"] == ResourceCategory.ARTICLE

    def test_filter_by_featured(self, api_client, admin_user):
        """Test filtering by featured status."""
        Resource.objects.create(
            title="Featured Article",
            content="Content",
            featured=True,
            status=ResourceStatus.PUBLISHED,
        )
        Resource.objects.create(
            title="Regular Article",
            content="Content",
            featured=False,
            status=ResourceStatus.PUBLISHED,
        )

        url = reverse("resource-list")
        response = api_client.get(url, {"featured": "true"})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["data"]) == 1
        assert response.data["data"][0]["featured"] is True

    def test_search_resources(self, api_client, admin_user):
        """Test full-text search."""
        Resource.objects.create(
            title="Python Article",
            content="Content about Python programming",
            status=ResourceStatus.PUBLISHED,
        )
        Resource.objects.create(
            title="JavaScript Article",
            content="Content about JavaScript",
            status=ResourceStatus.PUBLISHED,
        )

        url = reverse("resource-list")
        response = api_client.get(url, {"search": "Python"})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["data"]) == 1
        assert "Python" in response.data["data"][0]["title"]


class TestCategoriesAPI:
    """Test the categories endpoint."""

    def test_categories_public_access(self, api_client, admin_user):
        """Test that categories endpoint is publicly accessible."""
        # Create resources in different categories
        Resource.objects.create(
            title="Article 1",
            content="Content",
            category=ResourceCategory.ARTICLE,
            status=ResourceStatus.PUBLISHED,
        )
        Resource.objects.create(
            title="Article 2",
            content="Content",
            category=ResourceCategory.ARTICLE,
            status=ResourceStatus.PUBLISHED,
        )
        Resource.objects.create(
            title="News 1",
            content="Content",
            category=ResourceCategory.NEWS,
            status=ResourceStatus.PUBLISHED,
        )

        url = reverse("resource-categories")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True

        # Find article category in response
        article_category = next(
            c
            for c in response.data["data"]
            if c["category"] == ResourceCategory.ARTICLE
        )
        assert article_category["count"] == 2

        news_category = next(
            c for c in response.data["data"] if c["category"] == ResourceCategory.NEWS
        )
        assert news_category["count"] == 1

    def test_categories_counts_only_published(self, api_client, admin_user):
        """Test that categories only count published resources."""
        Resource.objects.create(
            title="Published Article",
            content="Content",
            category=ResourceCategory.ARTICLE,
            status=ResourceStatus.PUBLISHED,
        )
        Resource.objects.create(
            title="Draft Article",
            content="Content",
            category=ResourceCategory.ARTICLE,
            status=ResourceStatus.DRAFT,
        )

        url = reverse("resource-categories")
        response = api_client.get(url)

        article_category = next(
            c
            for c in response.data["data"]
            if c["category"] == ResourceCategory.ARTICLE
        )
        # Should only count published (1), not draft
        assert article_category["count"] == 1


class TestMediaFileAPI:
    """Test the media file upload endpoints."""

    def test_upload_file_admin(self, api_client, admin_user):
        """Test that admin users can upload files."""
        api_client.force_authenticate(user=admin_user)
        url = reverse("mediafile-list")

        # Create a test file
        image_data = BytesIO(b"fake jpeg data")
        file_data = {
            "file": SimpleUploadedFile(
                "test.jpg", image_data.read(), content_type="image/jpeg"
            )
        }

        response = api_client.post(url, file_data, format="multipart")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["success"] is True
        assert MediaFile.objects.count() == 1

    def test_upload_invalid_file_type(self, api_client, admin_user):
        """Test that invalid file types are rejected."""
        api_client.force_authenticate(user=admin_user)
        url = reverse("mediafile-list")

        file_data = {
            "file": SimpleUploadedFile(
                "test.txt", b"fake text data", content_type="text/plain"
            )
        }

        response = api_client.post(url, file_data, format="multipart")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["success"] is False

    def test_upload_file_too_large(self, api_client, admin_user):
        """Test that files over 5MB are rejected."""
        api_client.force_authenticate(user=admin_user)
        url = reverse("mediafile-list")

        # Create a file larger than 5MB
        large_data = b"x" * (6 * 1024 * 1024)  # 6MB
        file_data = {
            "file": SimpleUploadedFile(
                "large.jpg", large_data, content_type="image/jpeg"
            )
        }

        response = api_client.post(url, file_data, format="multipart")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "too large" in response.data["message"].lower()

    def test_upload_file_public_unauthorized(self, api_client):
        """Test that public users cannot upload files."""
        url = reverse("mediafile-list")

        image_data = BytesIO(b"fake jpeg data")
        file_data = {
            "file": SimpleUploadedFile(
                "test.jpg", image_data.read(), content_type="image/jpeg"
            )
        }

        response = api_client.post(url, file_data, format="multipart")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_media_file_admin(self, api_client, admin_user, sample_media_file):
        """Test that admin users can delete media files."""
        api_client.force_authenticate(user=admin_user)
        url = reverse("mediafile-detail", kwargs={"pk": sample_media_file.pk})

        response = api_client.delete(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True
        assert MediaFile.objects.count() == 0

    def test_delete_media_file_owner(self, api_client, admin_user, sample_media_file):
        """Test that file owners can delete their own files."""
        api_client.force_authenticate(user=admin_user)
        url = reverse("mediafile-detail", kwargs={"pk": sample_media_file.pk})

        response = api_client.delete(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True


class TestResourceValidation:
    """Test resource validation rules."""

    def test_tags_max_10(self, api_client, admin_user):
        """Test that maximum 10 tags are allowed."""
        api_client.force_authenticate(user=admin_user)
        url = reverse("resource-list")
        data = {
            "title": "Test Article",
            "content": "Content",
            "tags": [
                "tag1",
                "tag2",
                "tag3",
                "tag4",
                "tag5",
                "tag6",
                "tag7",
                "tag8",
                "tag9",
                "tag10",
                "tag11",
            ],
        }

        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_duplicate_slug_handling(self, api_client, admin_user):
        """Test that duplicate slugs are handled automatically."""
        api_client.force_authenticate(user=admin_user)
        url = reverse("resource-list")

        # Create first resource
        data1 = {
            "title": "Same Title",
            "content": "Content 1",
            "category": ResourceCategory.ARTICLE,
        }
        response1 = api_client.post(url, data1)
        assert response1.status_code == status.HTTP_201_CREATED
        slug1 = response1.data["data"]["slug"]

        # Create second resource with same title
        data2 = {
            "title": "Same Title",
            "content": "Content 2",
            "category": ResourceCategory.ARTICLE,
        }
        response2 = api_client.post(url, data2)
        assert response2.status_code == status.HTTP_201_CREATED
        slug2 = response2.data["data"]["slug"]

        # Slugs should be different
        assert slug1 != slug2
        assert slug2.startswith(slug1)
