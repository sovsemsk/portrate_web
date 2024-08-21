from django.contrib.admin import StackedInline, site
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Profile


class ProfileInline(StackedInline):
    model = Profile
    can_delete = False
    fk_name = "user"
    fields = [
        "api_secret",
        "telegram_id",
        "default_timezone",
        "rate",
        "balance",
        "start_price_monthly_base",
        "regular_price_monthly_base",
        "business_price_monthly_base",
        "start_max_count",
        "regular_max_count",
        "business_max_count"
    ]

    readonly_fields = ["api_secret", "telegram_id"]
    verbose_name_plural = "профиль"


class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline]


site.unregister(User)
site.register(User, CustomUserAdmin)

