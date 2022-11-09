from django.contrib import admin

# Register your models here.
from .models import Investment, InvestmentRoom, Gallery, Investors,


class InvestmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'auth_provider', 'created_at']


admin.site.register(InvestmentRoom, Investment)
