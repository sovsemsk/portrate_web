from django.contrib.admin import ModelAdmin, register, TabularInline

from .models import Company, Membership, Payment


class MembershipInlineAdmin(TabularInline):
    autocomplete_fields = ["user"]
    fields = ["user", "is_owner"]
    model = Membership


@register(Company)
class CompanyAdmin(ModelAdmin):
    fields = ["name", "address", "phone"]
    inlines = [MembershipInlineAdmin]
    list_display = ["name"]
    readonly_fields = ["name", "address", "phone"]
    search_fields = ["name"]

    def has_add_permission(self, request):
        return False


@register(Payment)
class PaymentAdmin(ModelAdmin):
    fields = ["user", "rate", "period", "amount", "is_paid" ]
    list_display = ["user", "created_at", "paid_at", "amount", "is_paid"]
    list_filter = ["is_paid", "created_at", "paid_at"]
    readonly_fields = ["amount", "is_paid", "period", "rate", "user"]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
