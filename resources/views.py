"""
Views for the resources app.
"""

from django.db.models import Count, Q
from django.contrib.postgres.search import SearchQuery, SearchVector
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from .models import Resource, MediaFile, ResourceCategory, ResourceStatus
from .serializers import (
    ResourceSerializer,
    ResourceCreateUpdateSerializer,
    ResourceListSerializer,
    MediaFileSerializer,
    CategoryCountSerializer,
)
from .permissions import IsAdminOrEditor, ReadOnly


class StandardResultsSetPagination:
    """
    Custom pagination class with configurable page size.
    
    Query parameters:
    - page: Page number (default: 1)
    - per_page: Items per page (default: 10, max: 100)
    """
    
    default_page_size = 10
    max_page_size = 100
    page_query_param = 'page'
    page_size_query_param = 'per_page'


class ResourceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Resource model.
    
    Provides CRUD operations with filtering, search, and pagination.
    
    ## Permissions
    - List/Retrieve: Public (read-only)
    - Create/Update/Delete: Admin or Editor only
    
    ## Filters
    - category: Filter by category (article, disclosure, news, actions)
    - status: Filter by status (draft, pending, approved, published, archived)
    - featured: Filter by featured status (true/false)
    - search: Full-text search in title and content
    - author: Filter by author name
    
    ## Pagination
    - page: Page number
    - per_page: Items per page (max: 100)
    """
    
    queryset = Resource.objects.all()
    lookup_field = 'slug'
    
    def get_permissions(self):
        """Return appropriate permissions based on action."""
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsAdminOrEditor]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action in ['create', 'update', 'partial_update']:
            return ResourceCreateUpdateSerializer
        elif self.action == 'list':
            return ResourceListSerializer
        return ResourceSerializer
    
    def get_queryset(self):
        """
        Return filtered queryset based on query parameters.
        
        Public users only see published resources.
        Staff can see all resources.
        """
        queryset = Resource.objects.all()
        
        # Get query parameters
        category = self.request.query_params.get('category')
        status_param = self.request.query_params.get('status')
        featured = self.request.query_params.get('featured')
        search = self.request.query_params.get('search')
        author = self.request.query_params.get('author')
        
        # Filter by category
        if category:
            queryset = queryset.filter(category=category)
        
        # Filter by status
        # Public users can only see published resources
        if not self.request.user.is_staff:
            queryset = queryset.filter(status=ResourceStatus.PUBLISHED)
        elif status_param:
            queryset = queryset.filter(status=status_param)
        
        # Filter by featured
        if featured is not None:
            is_featured = featured.lower() in ['true', '1', 'yes']
            queryset = queryset.filter(featured=is_featured)
        
        # Filter by author
        if author:
            queryset = queryset.filter(
                Q(author_name__icontains=author) |
                Q(author_user__username__icontains=author) |
                Q(author_user__email__icontains=author)
            )
        
        # Full-text search
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(content__icontains=search) |
                Q(excerpt__icontains=search)
            )
        
        return queryset.select_related('author_user')
    
    def list(self, request, *args, **kwargs):
        """
        List resources with pagination and filtering.
        
        Returns wrapped response with success flag and metadata.
        """
        queryset = self.get_queryset()
        
        # Manual pagination handling
        page = int(request.query_params.get('page', 1))
        per_page = int(request.query_params.get('per_page', 10))
        
        # Enforce max page size
        per_page = min(per_page, StandardResultsSetPagination.max_page_size)
        
        # Calculate pagination
        total = queryset.count()
        start = (page - 1) * per_page
        end = start + per_page
        
        # Get paginated queryset
        paginated_queryset = queryset[start:end]
        
        # Serialize
        serializer = self.get_serializer(paginated_queryset, many=True)
        
        # Calculate total pages
        total_pages = (total + per_page - 1) // per_page
        
        return Response({
            'success': True,
            'message': 'Resources retrieved successfully',
            'data': serializer.data,
            'meta': {
                'current_page': page,
                'per_page': per_page,
                'total': total,
                'total_pages': total_pages,
            }
        })
    
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a single resource by slug."""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        return Response({
            'success': True,
            'message': 'Resource retrieved successfully',
            'data': serializer.data
        })
    
    def create(self, request, *args, **kwargs):
        """Create a new resource."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Set author if not provided
        if not serializer.validated_data.get('author_name') and request.user:
            serializer.validated_data['author_user'] = request.user
        
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response({
            'success': True,
            'message': 'Resource created successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, *args, **kwargs):
        """Update a resource (full update)."""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response({
            'success': True,
            'message': 'Resource updated successfully',
            'data': serializer.data
        })
    
    def partial_update(self, request, *args, **kwargs):
        """Partially update a resource."""
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """Delete a resource."""
        instance = self.get_object()
        self.perform_destroy(instance)
        
        return Response({
            'success': True,
            'message': 'Resource deleted successfully'
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def categories(self, request):
        """
        Get all categories with resource counts.
        
        Returns categories and the count of published resources in each.
        """
        categories = []
        
        # Get counts for each category
        category_counts = Resource.objects.filter(
            status=ResourceStatus.PUBLISHED
        ).values('category').annotate(
            count=Count('id')
        ).order_by('category')
        
        # Build response
        count_map = {item['category']: item['count'] for item in category_counts}
        
        for category_value, display_name in ResourceCategory.choices:
            categories.append({
                'category': category_value,
                'display_name': display_name,
                'count': count_map.get(category_value, 0)
            })
        
        return Response({
            'success': True,
            'message': 'Categories retrieved successfully',
            'data': categories
        })


class MediaFileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for MediaFile model.
    
    Provides file upload and management capabilities.
    
    ## Permissions
    - List/Retrieve: Admin or Editor only
    - Create/Update/Delete: Admin or Editor only
    
    ## File Validation
    - Allowed types: JPEG, PNG, GIF, WebP
    - Max size: 5MB
    """
    
    queryset = MediaFile.objects.all()
    serializer_class = MediaFileSerializer
    permission_classes = [IsAuthenticated, IsAdminOrEditor]
    
    ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
    
    def get_queryset(self):
        """Return media files filtered by user if not staff."""
        queryset = MediaFile.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(uploaded_by=self.request.user)
        return queryset.select_related('uploaded_by', 'resource')
    
    def create(self, request, *args, **kwargs):
        """Upload a new media file with validation."""
        file_obj = request.FILES.get('file')
        
        if not file_obj:
            return Response({
                'success': False,
                'message': 'No file provided'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate file type
        if file_obj.content_type not in self.ALLOWED_TYPES:
            return Response({
                'success': False,
                'message': f'Invalid file type. Allowed: JPEG, PNG, GIF, WebP'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate file size
        if file_obj.size > self.MAX_FILE_SIZE:
            return Response({
                'success': False,
                'message': f'File too large. Max size: 5MB'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Prepare data
        data = {
            'file': file_obj,
            'uploaded_by': request.user.id,
        }
        
        # Optional resource association
        resource_id = request.data.get('resource')
        if resource_id:
            data['resource'] = resource_id
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response({
            'success': True,
            'message': 'File uploaded successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED, headers=headers)
    
    def destroy(self, request, *args, **kwargs):
        """Delete a media file."""
        instance = self.get_object()
        
        # Check permission (only uploader or staff can delete)
        if not request.user.is_staff and instance.uploaded_by != request.user:
            return Response({
                'success': False,
                'message': 'Permission denied'
            }, status=status.HTTP_403_FORBIDDEN)
        
        self.perform_destroy(instance)
        
        return Response({
            'success': True,
            'message': 'File deleted successfully'
        }, status=status.HTTP_200_OK)
