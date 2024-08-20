from django.contrib import admin
from .models import CustomUser, Balance, Subscription


# Register your models here.


class BalanceInline(admin.TabularInline):
    model = Balance

class SubscriptionInline(admin.TabularInline):
    model = Subscription

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    inlines = [
        BalanceInline,
        SubscriptionInline,
    ]

@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    pass

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'count_courses']
    list_display_links = ['user']

