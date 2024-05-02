import json

from django.core.serializers.json import DjangoJSONEncoder
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods

from resources.models import Company, Review


@require_http_methods(["GET"])
def rating(request, company_api_secret):
    company = get_object_or_404(Company, api_secret=company_api_secret)
    theme = request.GET.get("theme", "l")
    position = request.GET.get("position", "lb")

    return render(
        request,
        "widget/rating.js",
        {
            "api_secret": company_api_secret,
            "rating": str(company.rating).replace(",", "."),
            "reviews_total_count": company.reviews_total_count,
            "position": position,
            "stars_svg": company.stars_svg,
            "theme": theme
        },
        content_type="application/javascript"
    )


@require_http_methods(["GET"])
def reviews(request, company_api_secret):
    company = get_object_or_404(Company, api_secret=company_api_secret)
    company_reviews = Review.objects.filter(company_id=company.id, is_visible=True).order_by("-created_at")[:15]

    layout = request.GET.get("layout", "s")
    theme = request.GET.get("theme", "l")

    return render(
        request,
        f"widget/reviews_{'slider' if layout=='s' else 'grid'}.js",
        {
            "api_secret": company_api_secret,
            "layout": layout,
            "rating_yandex": str(company.rating_yandex).replace(",", "."),
            "rating_gis": str(company.rating_gis).replace(",", "."),
            "rating_google": str(company.rating_google).replace(",", "."),
            "reviews_yandex_total_count": str(company.reviews_yandex_total_count),
            "reviews_gis_total_count": str(company.reviews_gis_total_count),
            "reviews_google_total_count": str(company.reviews_google_total_count),
            "parser_link_yandex": company.parser_link_yandex,
            "parser_link_gis": company.parser_link_gis,
            "parser_link_google": company.parser_link_google,
            "reviews": company_reviews,
            "stars_svg_yandex": str(company.stars_svg_yandex).replace(",", "."),
            "stars_svg_gis": str(company.stars_svg_gis).replace(",", "."),
            "stars_svg_google": str(company.stars_svg_google).replace(",", "."),
            "theme": theme
        },
        content_type="application/javascript"
    )


@require_http_methods(["GET"])
def reviews_json(request, company_api_secret):
    company = get_object_or_404(Company, api_secret=company_api_secret)
    company_reviews = Review.objects.filter(company_id=company.id, is_visible=True).order_by("-created_at")[:15]
    theme = request.GET.get("theme", "l")

    data = {
        "rating": str(company.rating).replace(",", "."),
        "reviews_total_count": company.reviews_total_count,
        "reviews": [model_to_dict(review) for review in company_reviews],
        "stars_svg": company.stars_svg,
        "theme": theme
    },

    response = HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')
    response["Access-Control-Allow-Origin"] = "*"
    return response
