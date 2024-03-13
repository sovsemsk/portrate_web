from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    fk_name = "user"
    fields = (
        "api_secret",
        "telegram_id",
        "default_timezone",
        "can_notify_at_start",
        "can_notify_at_end",
        "can_notify_negative_portrate",
        "can_notify_negative_yandex",
        "can_notify_negative_gis",
        "can_notify_negative_google"
    )

    readonly_fields = (
        "api_secret",
        "telegram_id",
    )

    verbose_name_plural = "профиль"


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
