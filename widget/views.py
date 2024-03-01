from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods

from resources.models import Company


@require_http_methods(["GET"])
def rate(request, company_api_secret):
    company = get_object_or_404(Company, api_secret=company_api_secret, is_active=True)
    company_stars_percentage = int((float(company.portrate_rate) / 5.0) * 100)
    company_reviews_count = company.total_positive_count + company.total_negative_count

    theme = request.GET.get("theme", "light")
    position = request.GET.get("position", "lb")

    return render(
        request,
        "widget/rate.js",
        {
            "company_rate": str(company.portrate_rate).replace(",", "."),
            "company_stars_percentage": company_stars_percentage,
            "company_reviews_count": company_reviews_count,
            "theme": theme,
            "position": position
        },
        content_type="application/javascript"
    )
