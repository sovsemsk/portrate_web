from datetime import datetime, timedelta

from django.forms import Select
from django_filters import FilterSet, DateFromToRangeFilter, ChoiceFilter
from django_filters.widgets import DateRangeWidget

from resources.models import Message, Review, Service, Stars, RatingStamp


class MessageFilter(FilterSet):
    created_at = DateFromToRangeFilter(widget=DateRangeWidget(attrs={"class": "bp5-input", "type": "date"}))

    class Meta:
        model = Message
        fields = ["created_at"]


class ReviewFilter(FilterSet):
    created_at = DateFromToRangeFilter(widget=DateRangeWidget(attrs={"class": "bp5-input", "type": "date"}))
    service = ChoiceFilter(choices=Service, empty_label="Все источники", widget=Select())
    stars = ChoiceFilter(choices=Stars, empty_label="Все звезды", widget=Select())

    class Meta:
        model = Review
        fields = ["created_at", "service", "stars"]


class ReviewCountFilter(FilterSet):
    created_at = DateFromToRangeFilter(widget=DateRangeWidget(attrs={"class": "bp5-input", "type": "date"}))

    class Meta:
        model = Review
        fields = ["created_at"]

    @property
    def qs(self):
        parent_qs = super().qs
        range_param = self.data.get("range", "week")

        if range_param == "week":
            date_week_ago = datetime.today() - timedelta(days=7)
            parent_qs = parent_qs.filter(created_at__gte=date_week_ago, created_at__lte=datetime.today())

        return parent_qs

class RatingStampFilter(FilterSet):
    created_at = DateFromToRangeFilter(widget=DateRangeWidget(attrs={"class": "bp5-input", "type": "date"}))

    class Meta:
        model = RatingStamp
        fields = ["created_at"]

    @property
    def qs(self):
        parent_qs = super().qs
        range_param = self.data.get("range", "week")

        if range_param == "week":
            date_week_ago = datetime.today() - timedelta(days=7)
            parent_qs = parent_qs.filter(created_at__gt=date_week_ago, created_at__lte=datetime.today())

        elif range_param == "month":
            return parent_qs.filter(created_at__iso_week_day__in=[1,3,7]).order_by("created_at")

        elif range_param == "quarter":
            return parent_qs.filter(created_at__iso_week_day=1).order_by("created_at")

        elif range_param == "year":
            return parent_qs.filter(created_at__day=1).order_by("created_at")

        elif range_param == "all":
            return parent_qs.filter(created_at__day=1, created_at__month__in=[1, 5, 9]).order_by("created_at")

        return parent_qs.order_by("created_at")
