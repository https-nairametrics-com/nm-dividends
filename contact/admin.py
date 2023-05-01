from django.contrib import admin

# Register your models here.
from .models import Contact


class ContactAdmin(admin.ModelAdmin):
    list_display = ['subject', 'message', 'created_at']


admin.site.register(Contact, ContactAdmin)
