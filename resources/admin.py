from django.contrib.admin import ModelAdmin, register, TabularInline

from .models import Company, Membership, Payment


class MembershipInlineAdmin(TabularInline):
    autocomplete_fields = ["user"]
    fields = ["user", "is_owner"]
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


@register(Payment)
class PaymentAdmin(ModelAdmin):
    list_display = ["user", "created_at", "paid_at","is_paid"]
    fields = ["rate", "period", "amount", "user", "is_paid"]
    readonly_fields = ["rate", "period", "amount", "user", "is_paid"]

    def has_add_permission(self, request):
        return False
