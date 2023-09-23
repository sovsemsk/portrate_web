from django.contrib import admin
from .models import PhoneMessage, EmailMessage, TelegramMessage, WhatsappMessage

admin.site.register(PhoneMessage) 
admin.site.register(EmailMessage)
admin.site.register(TelegramMessage)
admin.site.register(WhatsappMessage)