from django.contrib.admin import ModelAdmin, register, TabularInline

from .models import Company, Membership


class MembershipInlineAdmin(TabularInline):
    autocomplete_fields = ["user"]
    fields = ["user"]
    model = Membership


@register(Company)
class CompanyAdmin(ModelAdmin):
    inlines = [MembershipInlineAdmin]
    list_display = ["name", "is_active", "is_parse_yandex", "is_parse_gis", "is_parse_google"]
    list_filter = ["is_active", "is_parse_yandex", "is_parse_gis", "is_parse_google"]
    fieldsets = [
        [
            "Данные компании",
            {
                "fields": ["is_active", "logo", "name", "address", "phone"]
            },
        ],
        [
            "Парсер",
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
        ],
        [
            "Запрос отзыва",
            {
                "classes": ["collapse"],
                "fields": [
                    "form_link_yandex",
                    "form_link_gis",
                    "form_link_google",
                    "form_link_dikidi",
                    "form_link_restoclub",
                    "form_link_tripadvisor",
                    "form_link_prodoctorov",
                    "form_link_flamp",
                    "form_link_zoon",
                    "form_link_otzovik",
                    "form_link_irecommend"
                ]
            }
        ],
        [
            "Контактные данные",
            {
                "classes": ["collapse"],
                "fields": [
                    "form_contact_whatsapp",
                    "form_contact_telegram",
                    "form_contact_viber",
                    "form_contact_website",
                    "form_contact_vk",
                    "form_contact_ok",
                    "form_contact_facebook",
                    "form_contact_instagram",
                    "form_contact_youtube",
                    "form_contact_x"
                ],
            },
        ]
    ]
    readonly_fields = ["api_secret"]
    search_fields = ["name"]
