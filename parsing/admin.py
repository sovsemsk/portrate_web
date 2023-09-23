from django.contrib import admin
from .models import ReviewsParser, RatingParser

admin.site.register(ReviewsParser) 
admin.site.register(RatingParser)