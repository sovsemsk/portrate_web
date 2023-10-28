from django.contrib import admin
from .models import Company, NegativeMessage, Notification


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(NegativeMessage)
class NegativeMessageAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'company', 'phone', 'text']
    fields = ['company', 'phone', 'text']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    pass


'''
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
'''
