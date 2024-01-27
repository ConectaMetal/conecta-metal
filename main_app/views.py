from django.http.response import Http404
from django.shortcuts import render, get_object_or_404
from main_app.models import Products, Companies

# Create your views here.
def home(request):

    search_term = request.GET.get('search', '').strip()

    if not search_term:
        products = Products.objects.filter(
            company__isPartner=True
        ).order_by('-id')
    else:
        products = Products.objects.filter(
            company__isPartner=True,
            name__icontains=search_term
        )

    context = {
        'products': products, 
        'show_products': True,
        'search_term': search_term,
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
    context = {'company': company, 'products': products}

    return render(request=request, template_name='main/pages/company.html', context=context)

def sign(request):
    context = {
        'is_sign_page': True,
    }
    return render(request=request, template_name='main/pages/sign.html', context=context)


def search(request):
    

    
    
    return render(request=request, template_name='main/pages/home.html')