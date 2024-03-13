from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods

from resources.models import Company, Review


@require_http_methods(["GET"])
def rate(request, company_api_secret):
    company = get_object_or_404(Company, api_secret=company_api_secret, is_active=True)

    theme = request.GET.get("theme", "l")
    position = request.GET.get("position", "lb")

    return render(
        request,
        "widget/rate.js",
        {
            "rating": str(company.rating).replace(",", "."),
            "reviews_total_count": company.reviews_total_count,
            "theme": theme,
            "position": position
        },
        content_type="application/javascript"
    )


@require_http_methods(["GET"])
def reviews(request, company_api_secret):
    company = get_object_or_404(Company, api_secret=company_api_secret, is_active=True)
    company_reviews = Review.objects.filter(company_id=company.id, is_hidden=False).order_by("-created_at")[:15]
    theme = request.GET.get("theme", "l")

    return render(
        request,
        "widget/reviews.js",
        {
            "rating": str(company.rating).replace(",", "."),
            "reviews_total_count": company.reviews_total_count,
            "reviews": company_reviews,
            "theme": theme
        },
        content_type="application/javascript"
    )
