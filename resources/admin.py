from django.contrib import admin

from .models import Company, Review, Message


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ["name", "is_active"]
    readonly_fields = ["api_secret"]
    fieldsets = [
        ("КОНТЕНТ", {"fields": ["name", "address", "logo"]}),
        (
            "НАСТРОЙКИ",
            {
                "classes": ["collapse"],
                "fields": [
                    "is_active",
                    "is_first_parsing",
                    "api_secret",
                    "users"
                ],
            },
        ),
        (
            "ПАРСЕР",
            {
                "classes": ["collapse"],
                "fields": [
                    "is_parse_yandex",
                    "parser_link_yandex",
                    "is_parse_gis",
                    "parser_link_gis",
                    "is_parse_google",
                    "parser_link_google"
                ],
            },
        ),
        (
            "ФОРМА ЗАПРОСА ОТЗЫВА",
            {
                "classes": ["collapse"],
                "fields": [
                    "form_link_yandex",
                    "form_link_gis",
                    "form_link_google",
                    "form_link_mapsme",
                    "form_link_dikidi",
                    "form_link_restoclub",
                    "form_link_tripadvisor",
                    "form_link_prodoctorov",
                    "form_link_flamp",
                    "form_link_zoon",
                    "form_link_otzovik",
                    "form_link_irecommend"
                ],
            },
        )
    ]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["created_at", "company", "name", "is_hidden", "stars"]
    list_filter = ["company", "service"]
    readonly_fields = ["created_at", "stars", "remote_id"]
    fieldsets = [
        ("КОНТЕНТ", {"fields": ["name", "text"]}),
        ("НАСТРОЙКИ", {"classes": ["collapse"], "fields": ["company", "service", "is_hidden"]}),
        ("ДАННЫЕ", {"classes": ["collapse"], "fields": ["created_at", "stars", "remote_id"]}),
    ]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["created_at", "company", "phone"]
    list_filter = ["company"]
    readonly_fields = ["created_at"]
    fieldsets = [
        ("КОНТЕНТ", {"fields": ["text"]}),
        ("ДАННЫЕ", {"classes": ["collapse"], "fields": ["created_at", "phone"]}),
        ("НАСТРОЙКИ", {"classes": ["collapse"], "fields": ["company"]}),
    ]

