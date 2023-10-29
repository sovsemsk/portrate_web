from django.contrib import admin
from .models import Company, NegativeMessage, Notification


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name']
    readonly_fields = [
        'portrate_rate',
        'portrate_negative_count',
        'yandex_rate',
        'yandex_positive_count',
        'yandex_negative_count',
        'gis_rate',
        'gis_positive_count',
        'gis_negative_count',
        'google_rate',
        'google_positive_count',
        'google_negative_count',
        'mapsme_rate',
        'mapsme_positive_count',
        'mapsme_negative_count',
        'dikidi_rate',
        'dikidi_positive_count',
        'dikidi_negative_count',
        'restoclub_rate',
        'restoclub_positive_count',
        'restoclub_negative_count',
        'tripadvisor_rate',
        'tripadvisor_positive_count',
        'tripadvisor_negative_count',
        'prodoctorov_rate',
        'prodoctorov_positive_count',
        'prodoctorov_negative_count',
        'flamp_rate',
        'flamp_positive_count',
        'zoon_rate',
        'zoon_positive_count',
        'zoon_negative_count',
        'otzovik_rate',
        'otzovik_positive_count',
        'otzovik_negative_count',
        'irecommend_rate',
        'irecommend_positive_count',
        'irecommend_negative_count'
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
                    'request_form_home_head',
                    'request_form_positive_head',
                    'request_form_negative_head',
                    'request_form_negative_text',
                    'request_form_tags',
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
                    'yandex_positive_count',
                    'yandex_negative_count',
                    'gis_rate',
                    'gis_positive_count',
                    'gis_negative_count',
                    'google_rate',
                    'google_positive_count',
                    'google_negative_count',
                    'mapsme_rate',
                    'mapsme_positive_count',
                    'mapsme_negative_count',
                    'dikidi_rate',
                    'dikidi_positive_count',
                    'dikidi_negative_count',
                    'restoclub_rate',
                    'restoclub_positive_count',
                    'restoclub_negative_count',
                    'tripadvisor_rate',
                    'tripadvisor_positive_count',
                    'tripadvisor_negative_count',
                    'prodoctorov_rate',
                    'prodoctorov_positive_count',
                    'prodoctorov_negative_count',
                    'flamp_rate',
                    'flamp_positive_count',
                    'zoon_rate',
                    'zoon_positive_count',
                    'zoon_negative_count',
                    'otzovik_rate',
                    'otzovik_positive_count',
                    'otzovik_negative_count',
                    'irecommend_rate',
                    'irecommend_positive_count',
                    'irecommend_negative_count',
                ]
            }
        ),

    ]


@ admin.register(NegativeMessage)
class NegativeMessageAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'company', 'phone', 'text']
    fields = ['company', 'phone', 'text']


@ admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    pass
