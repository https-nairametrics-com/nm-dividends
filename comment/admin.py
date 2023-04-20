from django.contrib import admin
from .models import Comment


# Register your models here.
class CommentAdmin(admin.ModelAdmin):
    list_display = ['comment', 'investment', 'investor', 'created_at']


admin.site.register(Comment, CommentAdmin)
