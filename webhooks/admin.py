from django.contrib import admin
from .models import TelegramSubscription


class TelegramSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['group', 'branch', 'telegram_user_id']
    list_filter = ['group__name', 'branch__name']
    fields = ['group', 'branch', 'telegram_user_id']
    readonly_fields = ['telegram_user_id']


admin.site.register(TelegramSubscription, TelegramSubscriptionAdmin)
