from django.contrib import admin
from .models import Company, NegativeMessage, Notification, Review


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name']
    readonly_fields = [
        'portrate_rate',
        'portrate_negative_count',

        'yandex_rate',
        'yandex_rate_count',
        'yandex_rate_stars',
        'yandex_positive_count',
        'yandex_negative_count',
        'yandex_rate_last_parse_at',
        'yandex_reviews_last_parse_at',

        'gis_rate',
        'gis_positive_count',
        'gis_negative_count',
        'gis_rate_last_parse_at',
        'gis_reviews_last_parse_at',

        'google_rate',
        'google_positive_count',
        'google_negative_count',
        'google_rate_last_parse_at',
        'google_reviews_last_parse_at',

        'mapsme_rate',
        'mapsme_positive_count',
        'mapsme_negative_count',
        'mapsme_rate_last_parse_at',
        'mapsme_reviews_last_parse_at',

        'dikidi_rate',
        'dikidi_positive_count',
        'dikidi_negative_count',
        'dikidi_rate_last_parse_at',
        'dikidi_reviews_last_parse_at',

        'restoclub_rate',
        'restoclub_positive_count',
        'restoclub_negative_count',
        'restoclub_rate_last_parse_at',
        'restoclub_reviews_last_parse_at',

        'tripadvisor_rate',
        'tripadvisor_positive_count',
        'tripadvisor_negative_count',
        'tripadvisor_rate_last_parse_at',
        'tripadvisor_reviews_last_parse_at',

        'prodoctorov_rate',
        'prodoctorov_positive_count',
        'prodoctorov_negative_count',
        'prodoctorov_rate_last_parse_at',
        'prodoctorov_reviews_last_parse_at',

        'flamp_rate',
        'flamp_positive_count',
        'flamp_negative_count',
        'flamp_rate_last_parse_at',
        'flamp_reviews_last_parse_at',

        'zoon_rate',
        'zoon_positive_count',
        'zoon_negative_count',
        'zoon_rate_last_parse_at',
        'zoon_reviews_last_parse_at',

        'otzovik_rate',
        'otzovik_positive_count',
        'otzovik_negative_count',
        'otzovik_rate_last_parse_at',
        'otzovik_reviews_last_parse_at',

        'irecommend_rate',
        'irecommend_positive_count',
        'irecommend_negative_count',
        'irecommend_rate_last_parse_at',
        'irecommend_reviews_last_parse_at',

        'total_negative_count',
        'total_positive_count'
    ]
    fieldsets = [
        (
            'КОНТЕНТ',
            {
                'fields': ['name', 'address', 'logo']
            }
        ),
        (
            'НАСТРОЙКИ',
            {
                'classes': ['collapse'],
                'fields': [
                    'is_active',
                    'users',
                    'yandex_id',
                    'is_yandex_reviews_upload',
                    'is_yandex_reviews_download',
                    'gis_id',
                    'is_gis_reviews_upload',
                    'is_gis_reviews_download',
                    'google_id',
                    'is_google_reviews_upload',
                    'is_google_reviews_download',
                    'mapsme_id',
                    'is_mapsme_reviews_upload',
                    'is_mapsme_reviews_download',
                    'dikidi_id',
                    'is_dikidi_reviews_upload',
                    'is_dikidi_reviews_download',
                    'restoclub_id',
                    'is_restoclub_reviews_upload',
                    'is_restoclub_reviews_download',
                    'tripadvisor_id',
                    'is_tripadvisor_reviews_upload',
                    'is_tripadvisor_reviews_download',
                    'prodoctorov_id',
                    'is_prodoctorov_reviews_upload',
                    'is_prodoctorov_reviews_download',
                    'flamp_id',
                    'is_flamp_reviews_upload',
                    'is_flamp_reviews_download',
                    'zoon_id',
                    'is_zoon_reviews_upload',
                    'is_zoon_reviews_download',
                    'otzovik_id',
                    'is_otzovik_reviews_upload',
                    'is_otzovik_reviews_download',
                    'irecommend_id',
                    'is_irecommend_reviews_upload',
                    'is_irecommend_reviews_download',

                ],
            },
        ),
        (
            'ФОРМА ЗАПРОСА ОТЗЫВА',
            {
                'classes': ['collapse'],
                'fields': [
                    'yandex_link',
                    'gis_link',
                    'google_link',
                    'mapsme_link',
                    'dikidi_link',
                    'restoclub_link',
                    'tripadvisor_link',
                    'prodoctorov_link',
                    'zoon_link',
                    'otzovik_link',
                    'irecommend_link',
                    'request_form_home_head',
                    'request_form_positive_head',
                    'request_form_negative_head',
                    'request_form_negative_text',
                    'request_form_tags',
                ],
            },
        ),
        (
            'ПОКАЗАТЕЛИ',
            {
                'fields': [
                    'portrate_rate',
                    'portrate_negative_count',

                    'yandex_rate',
                    'yandex_rate_count',
                    'yandex_rate_stars',
                    'yandex_positive_count',
                    'yandex_negative_count',
                    'yandex_rate_last_parse_at',
                    'yandex_reviews_last_parse_at',

                    'gis_rate',
                    'gis_positive_count',
                    'gis_negative_count',
                    'gis_rate_last_parse_at',
                    'gis_reviews_last_parse_at',

                    'google_rate',
                    'google_positive_count',
                    'google_negative_count',
                    'google_rate_last_parse_at',
                    'google_reviews_last_parse_at',

                    'mapsme_rate',
                    'mapsme_positive_count',
                    'mapsme_negative_count',
                    'mapsme_rate_last_parse_at',
                    'mapsme_reviews_last_parse_at',

                    'dikidi_rate',
                    'dikidi_positive_count',
                    'dikidi_negative_count',
                    'dikidi_rate_last_parse_at',
                    'dikidi_reviews_last_parse_at',

                    'restoclub_rate',
                    'restoclub_positive_count',
                    'restoclub_negative_count',
                    'restoclub_rate_last_parse_at',
                    'restoclub_reviews_last_parse_at',

                    'tripadvisor_rate',
                    'tripadvisor_positive_count',
                    'tripadvisor_negative_count',
                    'tripadvisor_rate_last_parse_at',
                    'tripadvisor_reviews_last_parse_at',

                    'prodoctorov_rate',
                    'prodoctorov_positive_count',
                    'prodoctorov_negative_count',
                    'prodoctorov_rate_last_parse_at',
                    'prodoctorov_reviews_last_parse_at',

                    'flamp_rate',
                    'flamp_positive_count',
                    'flamp_negative_count',
                    'flamp_rate_last_parse_at',
                    'flamp_reviews_last_parse_at',

                    'zoon_rate',
                    'zoon_positive_count',
                    'zoon_negative_count',
                    'zoon_rate_last_parse_at',
                    'zoon_reviews_last_parse_at',

                    'otzovik_rate',
                    'otzovik_positive_count',
                    'otzovik_negative_count',
                    'otzovik_rate_last_parse_at',
                    'otzovik_reviews_last_parse_at',

                    'irecommend_rate',
                    'irecommend_positive_count',
                    'irecommend_negative_count',
                    'irecommend_rate_last_parse_at',
                    'irecommend_reviews_last_parse_at',

                    'total_negative_count',
                    'total_positive_count'
                ]
            }
        ),

    ]


@ admin.register(NegativeMessage)
class NegativeMessageAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'company', 'phone']
    list_filter = ['company']
    readonly_fields = ['created_at']

    fieldsets = [
        (
            'КОНТЕНТ',
            {
                'fields': ['text']
            }
        ),
        (
            'ДАННЫЕ',
            {
                'classes': ['collapse'],
                'fields': ['created_at', 'phone']
            }
        ),
        (
            'НАСТРОЙКИ',
            {
                'classes': ['collapse'],
                'fields': ['company']
            }
        ),
    ]

@ admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'company', 'initiator']
    list_filter = ['company', 'initiator']
    readonly_fields = ['created_at']

    fieldsets = [
        (
            'КОНТЕНТ',
            {
                'fields': ['text']
            }
        ),
        (
            'ДАННЫЕ',
            {
                'classes': ['collapse'],
                'fields': ['created_at']
            }
        ),
        (
            'НАСТРОЙКИ',
            {
                'classes': ['collapse'],
                'fields': ['company', 'negative_message', 'initiator']
            }
        ),
    ]


@ admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'company', 'name']
    list_filter = ['company', 'service']

    readonly_fields = [
        'created_at',
        'remote_id'
    ]

    fieldsets = [
        (
            'КОНТЕНТ',
            {
                'fields': ['name', 'text', 'answer']
            }
        ),
        (
            'ДАННЫЕ',
            {
                'classes': ['collapse'],
                'fields': ['created_at', 'rate', 'remote_id', 'avatar_url']
            }
        ),
        (
            'НАСТРОЙКИ',
            {
                'classes': ['collapse'],
                'fields': ['company', 'service']
            }
        ),
    ]
