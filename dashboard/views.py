from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_http_methods
from resources.models import Branch, Company


@login_required
@require_http_methods(['GET'])
def index(request):
    return render(request, 'dashboard/index.html', {'nav': 'index'})


@login_required
@require_http_methods(['GET'])
def branches(request):
    companies = Company.objects.filter(users__in=(request.user,)).all()
    branches = Branch.objects.filter(company__in=companies).all()
    return render(request, 'dashboard/branches.html', {
        'nav': 'branches',
        'companies': companies,
        'branches': branches
    })
