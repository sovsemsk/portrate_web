from django.contrib import admin
from .models import NegativeMessage, NegativeReview

admin.site.register(NegativeMessage) 
admin.site.register(NegativeReview)