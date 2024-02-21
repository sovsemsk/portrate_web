from django.shortcuts import render
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
def javascript(request):
    return render(request, "widget/javascript.js", content_type="application/javascript")
