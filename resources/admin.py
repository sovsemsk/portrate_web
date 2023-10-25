from django.contrib import admin
from .models import Company, Branch, Website, WebsiteImage, WebsiteContact, WebsiteUrl, WebsiteCard, NegativeMessage, NegativeMessageTag, NegativeReview, PositiveReview


class BranchAdminInline(admin.StackedInline):
    model = Branch
    extra = 0
    fields = ['name', 'company']


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name']
    fields = ['name', 'users']
    inlines = [BranchAdminInline]


class WebsiteImageInline(admin.StackedInline):
    model = WebsiteImage
    extra = 0
    fields = ['name', 'file', 'sort', 'is_logo']


class WebsiteContactInline(admin.StackedInline):
    model = WebsiteContact
    extra = 0
    fields = ['platform', 'name', 'value']


class WebsiteUrlInline(admin.StackedInline):
    model = WebsiteUrl
    extra = 0
    fields = ['platform', 'name', 'value']


class WebsiteCardInline(admin.StackedInline):
    model = WebsiteCard
    extra = 0
    fields = ['platform', 'name', 'value']


@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    list_display = ['branch', 'name']
    list_filter = ['branch__name']
    fieldsets = [
        (
            'НАСТРОЙКИ',
            {
                'classes': ['collapse'],
                'fields': ['company', 'branch', 'path', 'is_published',],
            },
        ),
        (
            'КНОПКА ДЕЙСТВИЯ',
            {
                'classes': ['collapse',],
                'fields': ['action_button_text', 'action_button_url',],
            },
        ),
        (
            'ИНФОРМАЦИЯ',
            {
                'classes': ['collapse',],
                'fields': ['name', 'specialization', 'city', 'address', 'description',],
            },
        ),
        (
            'ГРАФИК РАБОТЫ',
            {
                'classes': ['collapse',],
                'fields': [
                    'monday_schedule',
                    'is_work_at_monday',
                    'tuesday_schedule',
                    'is_work_at_tuesday',
                    'wednesday_schedule',
                    'is_work_at_wednesday',
                    'thursday_schedule',
                    'is_work_at_thursday',
                    'friday_schedule',
                    'is_work_at_friday',
                    'saturday_schedule',
                    'is_work_at_saturday',
                    'sunday_schedule',
                    'is_work_at_sunday',
                ],
            },
        ),
    ]
    inlines = [
        WebsiteImageInline,
        WebsiteContactInline,
        WebsiteUrlInline,
        WebsiteCardInline
    ]


@admin.register(NegativeMessage)
class NegativeMessageAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'company', 'branch', 'phone', 'text']
    fields = ['company', 'branch', 'phone', 'text', 'negative_message_tag']


@admin.register(NegativeMessageTag)
class NegativeMessageTagAdmin(admin.ModelAdmin):
    list_display = ['text']
    fields = ['text']


@admin.register(NegativeReview)
class NegativeReviewAdmin(admin.ModelAdmin):
    pass


@admin.register(PositiveReview)
class PositiveReviewAdmin(admin.ModelAdmin):
    pass
