from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods

from resources.models import Company, Review


@require_http_methods(["GET"])
def reviews(request, company_api_secret):
    company = get_object_or_404(Company, api_secret=company_api_secret)
    reviews = Review.objects.filter(company_id=company.id, is_visible=True).order_by("-created_at")[:15]
    theme = request.GET.get("theme", "l")

    return render(
        request,
        "widget/reviews_slider.js",
        {
            "api_secret": company_api_secret,
            "company": company,
            "reviews": reviews,
            "theme": theme
        },
        content_type="application/javascript"
    )
