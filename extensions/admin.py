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
        "default_timezone"
    ]

    readonly_fields = ["api_secret", "telegram_id"]
    verbose_name_plural = "профиль"


class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline]


site.unregister(User)
site.register(User, CustomUserAdmin)

