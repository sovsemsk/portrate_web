from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods

from resources.models import Company, Review


@require_http_methods(["GET"])
def reviews(request, company_api_secret):
    company = get_object_or_404(Company, api_secret=company_api_secret)
    layout = request.GET.get("layout", "s")
    reviews = Review.objects.filter(company_id=company.id, is_visible=True).order_by("-created_at")[:15]
    theme = request.GET.get("theme", "l")

    return render(
        request,
        f"widget/reviews_{'slider' if layout=='s' else 'grid'}.js",
        {
            "api_secret": company_api_secret,
            "company": company,
            "layout": layout,
            "reviews": reviews,
            "theme": theme
        },
        content_type="application/javascript"
    )
