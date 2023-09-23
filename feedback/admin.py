from django.contrib import admin
from .models import NegativeMessage, NegativeReview, PositiveReview

admin.site.register(NegativeMessage) 
admin.site.register(NegativeReview)
admin.site.register(PositiveReview)