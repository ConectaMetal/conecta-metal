from django.shortcuts import render, get_object_or_404
from main_app.models import Products
from utils.main.rating import product_rating

# Create your views here.
def home(request):
    products = Products.objects.all().order_by('-id')
    context = {'products': products, 'product_rating': product_rating}
    return render(request=request, template_name='main/pages/home.html', context=context)


def product(request, slug):
    product = get_object_or_404(
        Products, slug=slug
    )
    context = {'product': product}

    return render(request=request, template_name='main/pages/product.html', context=context)