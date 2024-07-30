from django.db.models import Count
from django.forms import CheckboxSelectMultiple
from django_filters import FilterSet, DateFromToRangeFilter, MultipleChoiceFilter
from django_filters.widgets import DateRangeWidget

from resources.models import Message, Review, Service, Stars


class SwitchSelectMultiple(CheckboxSelectMultiple):
    option_template_name = "forms/widgets/switch_option.html"


class StarSelectMultiple(CheckboxSelectMultiple):
    option_template_name = "forms/widgets/star_option.html"


class MessageFilter(FilterSet):
    class Meta:
        model = Message
        fields = ["created_at", "visit_stamp__utm_source"]

    created_at = DateFromToRangeFilter(
        widget=DateRangeWidget(
            attrs={
                "class": "bp5-input",
                "form": "FILTER",
                "type": "date"
            }
        )
    )

    visit_stamp__utm_source = MultipleChoiceFilter(
        widget=SwitchSelectMultiple(
            attrs={
                "data-input": ""
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super(MessageFilter, self).__init__(*args, **kwargs)

        self.filters["visit_stamp__utm_source"].extra["choices"] = list(
            map(
                lambda visit_stamp: [visit_stamp["visit_stamp__utm_source"], visit_stamp["visit_stamp__utm_source"]],
                self.queryset.values(
                    "visit_stamp__utm_source"
                ).annotate(
                    count=Count("visit_stamp__utm_source")
                ).order_by("visit_stamp__utm_source")
            )
        )


class ReviewFilter(FilterSet):
    class Meta:
        fields = ["created_at", "service", "stars"]
        model = Review

    created_at = DateFromToRangeFilter(
        widget=DateRangeWidget(
            attrs={
                "class": "bp5-input",
                "form": "FILTER",
                "type": "date"
            }
        )
    )

    service = MultipleChoiceFilter(
        widget=SwitchSelectMultiple(
            attrs={
                "data-input": ""
            }
        )
    )

    stars = MultipleChoiceFilter(
        widget=StarSelectMultiple(
            attrs={
                "data-input": ""
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super(ReviewFilter, self).__init__(*args, **kwargs)

        self.filters["service"].extra["choices"] = list(
            map(
                lambda review: [
                    review["service"],
                    Service[review["service"]].label
                ],
                Review.objects.values("service").filter(
                    company_id=kwargs["request"].resolver_match.kwargs["company_pk"]
                ).annotate(
                    count=Count("service")
                ).order_by("service")
            )
        )

        self.filters['stars'].extra['choices'] = list(
            map(
                lambda review: [
                    review["stars"],
                    Stars[f"_{review['stars']}"].label
                ],
                Review.objects.values("stars").filter(
                    company_id=kwargs["request"].resolver_match.kwargs["company_pk"]
                ).annotate(
                    count=Count("stars")
                ).order_by("stars")
            )
        )
