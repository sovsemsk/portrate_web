from django.contrib.admin import ModelAdmin, register, TabularInline

from .models import Company, Membership, Payment, Story, StorySlide, InstructionSlide, Instruction


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
    fields = ["api_secret", "user", "rate", "period", "card_id", "amount", "is_paid" ]
    list_display = ["api_secret", "user", "created_at", "paid_at", "amount", "is_paid"]
    list_filter = ["is_paid", "created_at", "paid_at"]
    readonly_fields = ["amount", "is_paid", "period", "rate", "user"]
    search_fields = ["api_secret"]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class StorySlideInlineAdmin(TabularInline):
    fields = ["sort", "video", "image"]
    model = StorySlide


@register(Story)
class StoryAdmin(ModelAdmin):
    inlines = [StorySlideInlineAdmin]

    fieldsets = [
        (
            None,
            {
                "fields": ["name", "is_active", "preview"],
            },
        ),
        (
            "Разделы",
            {
                "fields": [
                    "is_visible_master",
                    "is_visible_finance",
                    "is_visible_user",
                    "is_visible_home",
                    "is_visible_statistic",
                    "is_visible_reviews",
                    "is_visible_messages",
                    "is_visible_widget",
                    "is_visible_feedback",
                    "is_visible_qr",
                    "is_visible_notifications"
                ],
            },
        ),
    ]

    list_display = ["name", "is_active"]

    list_filter = [
        "is_active",
        "is_visible_master",
        "is_visible_finance",
        "is_visible_user",
        "is_visible_home",
        "is_visible_statistic",
        "is_visible_reviews",
        "is_visible_messages",
        "is_visible_widget",
        "is_visible_feedback",
        "is_visible_qr",
        "is_visible_notifications"
    ]

    search_fields = ["name"]


class InstructionSlideInlineAdmin(TabularInline):
    fields = ["sort", "image", "description"]
    model = InstructionSlide


@register(Instruction)
class InstructionAdmin(ModelAdmin):
    inlines = [InstructionSlideInlineAdmin]

    fieldsets = [
        (
            None,
            {
                "fields": ["name", "is_active"],
            },
        ),
        (
            "Разделы",
            {
                "fields": [
                    "is_visible_yandex",
                    "is_visible_gis",
                    "is_visible_google",
                    "is_visible_avito",
                    "is_visible_zoon",
                    "is_visible_flamp",
                    "is_visible_yell",
                    "is_visible_prodoctorov",
                    "is_visible_yandex_services",
                    "is_visible_otzovik",
                    "is_visible_irecommend"
                ],
            },
        ),
    ]

    list_display = ["name", "is_active"]

    list_filter = [
        "is_active",
        "is_visible_yandex",
        "is_visible_gis",
        "is_visible_google",
        "is_visible_avito",
        "is_visible_zoon",
        "is_visible_flamp",
        "is_visible_yell",
        "is_visible_prodoctorov",
        "is_visible_yandex_services",
        "is_visible_otzovik",
        "is_visible_irecommend"
    ]

    search_fields = ["name"]
