from django.contrib import admin
from .models import NegativeMessageEvent, NegativeReviewEvent

admin.site.register(NegativeMessageEvent) 
admin.site.register(NegativeReviewEvent)