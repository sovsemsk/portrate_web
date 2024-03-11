from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods

from resources.models import Company, Review


@require_http_methods(["GET"])
def rate(request, company_api_secret):
    company = get_object_or_404(Company, api_secret=company_api_secret, is_active=True)
    company_rate_float_percentage = (13 / 100) * int(company.portrate_rate_float * 100)
    theme = request.GET.get("theme", "l")
    position = request.GET.get("position", "lb")

    return render(
        request,
        "widget/rate.js",
        {
            "company_rate": str(company.portrate_rate).replace(",", "."),
            "company_rate_ceil": int(company.portrate_rate_ceil),
            "company_rate_sub_rest": int(company.portrate_rate_ceil_sub_rest),
            "company_rate_float_percentage": str(company_rate_float_percentage).replace(",", "."),
            "company_reviews_count": company.total_reviews_count,
            "theme": theme,
            "position": position
        },
        content_type="application/javascript"
    )


@require_http_methods(["GET"])
def reviews(request, company_api_secret):
    company = get_object_or_404(Company, api_secret=company_api_secret, is_active=True)
    company_rate_float_percentage = (13 / 100) * int(company.portrate_rate_float * 100)
    company_reviews = Review.objects.filter(company_id=company.id, is_hidden=False).order_by("-created_at")[:15]
    theme = request.GET.get("theme", "l")

    return render(
        request,
        "widget/reviews.js",
        {
            "company_rate": str(company.portrate_rate).replace(",", "."),
            "company_rate_ceil": int(company.portrate_rate_ceil),
            "company_rate_sub_rest": int(company.portrate_rate_ceil_sub_rest),
            "company_rate_float_percentage": str(company_rate_float_percentage).replace(",", "."),
            "company_reviews": company_reviews,
            "company_reviews_count": company.total_reviews_count,
            "theme": theme
        },
        content_type="application/javascript"
    )
