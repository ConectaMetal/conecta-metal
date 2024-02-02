from django.http.response import Http404
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from main_app.models import Products, Companies, SocialMedia
from utils.pagination import make_pagination

import os

PER_PAGE = os.environ.get('PER_PAGE', 30)

# Create your views here.
def home(request):

    search_term = request.GET.get('q', '').strip()

    if not search_term:
        products = Products.objects.filter(
            company__isPartner=True
        ).order_by('-id')
        additional_query_string = ''
    else:
        products = Products.objects.filter(
            Q(name__icontains=search_term) |
            Q(details__icontains=search_term),
            company__isPartner=True,
        ).order_by('-id')
        additional_query_string = f'&q={search_term}'

    page_object, pagination_range = make_pagination(request, products, PER_PAGE)

    context = {
        'products': page_object, 
        'show_products': True,
        'search_term': search_term,
        'pagination_range': pagination_range,
        'additional_url_query': additional_query_string
    }

    return render(request=request, template_name='main/pages/home.html', context=context)


def product(request, slug):
    product = get_object_or_404(
        Products, slug=slug
    )
    context = {'product': product}

    return render(request=request, template_name='main/pages/product.html', context=context)


def company(request, slug):
    company = get_object_or_404(
        Companies, slug=slug
    )

    products = Products.objects.filter(
        company__id=company.id
    ).order_by('-id')

    social_medias = SocialMedia.objects.filter(
        company__id=company.id
    ).order_by('-id')

    context = {'company': company, 'products': products, 'social_medias': social_medias}

    return render(request=request, template_name='main/pages/company.html', context=context)


def sign(request):
    context = {
        'is_sign_page': True,
    }
    return render(request=request, template_name='main/pages/sign.html', context=context)

