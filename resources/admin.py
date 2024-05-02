from django.contrib.admin import ModelAdmin, register, TabularInline

from .models import Company, Membership


class MembershipInlineAdmin(TabularInline):
    autocomplete_fields = ["user"]
    fields = ["user"]
    model = Membership


@register(Company)
class CompanyAdmin(ModelAdmin):
    inlines = [MembershipInlineAdmin]
    list_display = ["name"]
    fields = ["name", "address", "phone"]
    readonly_fields = ["name", "address", "phone"]
    search_fields = ["name"]

    def has_add_permission(self, request):
        return False
