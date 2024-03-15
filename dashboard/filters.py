from django.forms import Select
from django_filters import FilterSet, DateFromToRangeFilter, ChoiceFilter
from django_filters.widgets import DateRangeWidget

from resources.models import Message, Review, Service, Stars


class MessageFilter(FilterSet):
    created_at = DateFromToRangeFilter(widget=DateRangeWidget(attrs={"class": "bp5-input", "type":"date"}))

    class Meta:
        model = Message
        fields = ["created_at"]


class ReviewFilter(FilterSet):
    service = ChoiceFilter(choices=Service, empty_label="Все источники", widget=Select())
    stars = ChoiceFilter(choices=Stars, empty_label="Все звезды", widget=Select())
    created_at = DateFromToRangeFilter(widget=DateRangeWidget(attrs={"class": "bp5-input", "type":"date"}))

    class Meta:
        model = Review
        fields = ["created_at", "service", "stars"]