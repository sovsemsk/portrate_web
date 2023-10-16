from django.contrib import admin
from .models import NegativeMessage, NegativeMessageTag, NegativeReview, PositiveReview


class NegativeMessageAdmin(admin.ModelAdmin):
    list_display = ['group', 'branch', 'phone', 'text']
    fields = ['group', 'branch', 'phone', 'text', 'negative_message_tag']


class NegativeMessageTagAdmin(admin.ModelAdmin):
    list_display = ['text']
    fields = ['text']


admin.site.register(NegativeMessage, NegativeMessageAdmin)
admin.site.register(NegativeMessageTag, NegativeMessageTagAdmin)

admin.site.register(NegativeReview)
admin.site.register(PositiveReview)
