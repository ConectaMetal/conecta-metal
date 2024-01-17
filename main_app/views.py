from django.shortcuts import render
from main_app.models import Products

# Create your views here.
def home(request):
    products = Products.objects.all().order_by('-id')
    context = {'products': products}
    return render(request=request, template_name='main/pages/home.html', context=context)


def product(request):
    return render(request=request, template_name='main/pages/product.html')