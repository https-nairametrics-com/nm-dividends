"""
Admin configuration for the resources app.
"""

from django.contrib import admin
from .models import Resource, MediaFile


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    """Admin configuration for Resource model."""
    
    list_display = [
        'title',
        'slug',
        'category',
        'status',
        'featured',
        'author',
        'date',
        'created_at',
    ]
    list_filter = [
        'category',
        'status',
        'featured',
        'created_at',
        'updated_at',
    ]
    search_fields = [
        'title',
        'content',
        'excerpt',
        'meta_title',
        'meta_description',
        'author_name',
        'author_user__email',
        'author_user__username',
    ]
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'content', 'excerpt')
        }),
        ('Categorization', {
            'fields': ('category', 'tags')
        }),
        ('Media', {
            'fields': ('featured_media', 'featured_media_type')
        }),
        ('Status & Workflow', {
            'fields': ('status', 'featured', 'date')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'og_image'),
            'classes': ('collapse',)
        }),
        ('Author', {
            'fields': ('author_name', 'author_user')
        }),
        ('External Link', {
            'fields': ('link',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def get_form(self, request, obj=None, **kwargs):
        """Customize form to add help text."""
        form = super().get_form(request, obj, **kwargs)
        if 'tags' in form.base_fields:
            form.base_fields['tags'].help_text = (
                "Enter tags as a JSON list, e.g., ['tag1', 'tag2']. Maximum 10 tags."
            )
        return form


@admin.register(MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    """Admin configuration for MediaFile model."""
    
    list_display = [
        'original_filename',
        'file_type',
        'file_size_display',
        'uploaded_by',
        'uploaded_at',
        'resource',
    ]
    list_filter = [
        'file_type',
        'uploaded_at',
    ]
    search_fields = [
        'original_filename',
        'uploaded_by__email',
        'uploaded_by__username',
    ]
    date_hierarchy = 'uploaded_at'
    ordering = ['-uploaded_at']
    readonly_fields = ['uploaded_at', 'file_size', 'file_type']
    
    fieldsets = (
        ('File Information', {
            'fields': ('file', 'original_filename', 'file_type', 'file_size')
        }),
        ('Upload Details', {
            'fields': ('uploaded_by', 'uploaded_at')
        }),
        ('Association', {
            'fields': ('resource',)
        }),
    )
    
    def file_size_display(self, obj):
        """Display file size in human-readable format."""
        if obj.file_size is None:
            return '-'
        
        size = obj.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} TB"
    
    file_size_display.short_description = 'File Size'
