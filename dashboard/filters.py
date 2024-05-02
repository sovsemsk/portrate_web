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
    service = ChoiceFilter(choices=Service, empty_label="Источник", widget=Select())
    stars = ChoiceFilter(choices=Stars, empty_label="Оценка", widget=Select())

    class Meta:
        model = Review
        fields = ["created_at", "service", "stars"]


class RatingStampFilter(FilterSet):

    class Meta:
        model = RatingStamp
        fields = []

    @property
    def qs(self):
        parent_qs = super().qs
        range_param = self.data.get("range", "week")

        if range_param == "week":
            parent_qs = parent_qs.filter(
                created_at__gt=datetime.today() - timedelta(days=7),
                created_at__lte=datetime.today()
            )

        elif range_param == "month":
            parent_qs = parent_qs.filter(
                created_at__gt=datetime.today() - timedelta(days=30),
                created_at__lte=datetime.today(),
                created_at__iso_week_day__in=[1, 3, 7]
            )

        elif range_param == "quarter":
            parent_qs = parent_qs.filter(
                created_at__gt=datetime.today() - timedelta(days=90),
                created_at__lte=datetime.today(),
                created_at__iso_week_day=1
            )

        elif range_param == "year":
            parent_qs = parent_qs.filter(
                created_at__gt=datetime.today() - timedelta(days=365),
                created_at__lte=datetime.today(),
                created_at__day=1
            )

        elif range_param == "total":
            parent_qs = parent_qs.filter(
                created_at__day=1,
                created_at__month__in=[1, 5, 9]
            )

        return parent_qs.order_by("created_at")
