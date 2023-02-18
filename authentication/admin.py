from django.contrib import admin

# Register your models here.
from .models import User, Referrals, Profile


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'auth_provider', 'created_at']


class InterestAdmin(admin.ModelAdmin):
    list_display = ['risk', 'owner', 'period',
                    'investmentsize', 'interest', 'created_at']


admin.site.register(User, UserAdmin)
admin.site.register(Referrals)
admin.site.register(Profile)
