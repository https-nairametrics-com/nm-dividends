from django.contrib import admin

# Register your models here.
from .models import Sponsor, SponsorInvestment, Currency, DealType, MainRoom, Investment, InvestmentRoom, Gallery, Investors


class InvestmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']

class InvestorAdmin(admin.ModelAdmin):
    list_display = ['amount', 'investment', 'created_at']

admin.site.register(Investment, InvestmentAdmin)
admin.site.register(MainRoom)
admin.site.register(InvestmentRoom)
admin.site.register(Gallery)
admin.site.register(Investors, InvestorAdmin)
admin.site.register(Currency)
admin.site.register(DealType)
admin.site.register(Sponsor)
admin.site.register(SponsorInvestment)
