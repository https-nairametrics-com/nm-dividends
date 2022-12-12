from django.contrib import admin

# Register your models here.
from .models import Currency, DealType, MainRoom, Investment, InvestmentRoom, Gallery, Investors


class InvestmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']


admin.site.register(Investment, InvestmentAdmin)
admin.site.register(MainRoom)
admin.site.register(InvestmentRoom)
admin.site.register(Gallery)
admin.site.register(Investors)
admin.site.register(Currency)
admin.site.register(DealType)
