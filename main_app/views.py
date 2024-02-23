from django.http.response import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from main_app.models import Products, Companies, SocialMedia, Services, UserProfile, ShoppingCart, Employee, Requests
from utils.pagination import make_pagination
from .forms import LoginForm, SignUpForm, AddToCartForm, RegisterCompanyForm

import os

PER_PAGE = int(os.environ.get('PER_PAGE', 30))

# Create your views here.
@login_required(login_url='main_app:login', redirect_field_name='next')
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

    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            existing_item = ShoppingCart.objects.filter(
                client=form.cleaned_data['client'],
                product=form.cleaned_data['product']
            ).exists()
            if not existing_item:
                form.save()
    else:
        form = AddToCartForm()
    form = AddToCartForm()

    user_profile = UserProfile.objects.filter(
        user=request.user
    ).first()

    cart_products = ShoppingCart.objects.filter(
        client__user = request.user
    ).order_by('-id')

    page_object, pagination_range = make_pagination(request, products, PER_PAGE)

    products_amount = 0
    for cart_product in cart_products:
        products_amount += cart_product.amount

    context = {
        'additional_url_query': additional_query_string,
        'form': form,
        'pagination_range': pagination_range,
        'products': page_object, 
        'products_amount': products_amount,
        'search_term': search_term,
        'show_products': True,
        'user_profile': user_profile,
    }

    return render(request=request, template_name='main/pages/home.html', context=context)


@login_required(login_url='main_app:login', redirect_field_name='next')
def product(request, slug):
    product = get_object_or_404(
        Products, slug=slug
    )

    cart_products = ShoppingCart.objects.filter(
        client__user = request.user
    ).order_by('-id')

    user_profile = UserProfile.objects.filter(
        user=request.user
    ).first()

    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            existing_item = ShoppingCart.objects.filter(
                client=form.cleaned_data['client'],
                product=form.cleaned_data['product']
            ).exists()
            if not existing_item:
                form.save()
    else:
        form = AddToCartForm()

    products_amount = 0
    for cart_product in cart_products:
        products_amount += cart_product.amount

    context = {
        'form': form,
        'product': product,
        'products_amount': products_amount,
        'user_profile': user_profile,
        }

    return render(request=request, template_name='main/pages/product.html', context=context)


@login_required(login_url='main_app:login', redirect_field_name='next')
def services(request):

    search_term = request.GET.get('q', '').strip()

    if not search_term:
        services = Services.objects.filter(
            company__isPartner=True
        ).order_by('-id')
        additional_query_string = ''
    else:
        services = Services.objects.filter(
            Q(name__icontains=search_term) |
            Q(details__icontains=search_term),
            company__isPartner=True,
        ).order_by('-id')
        additional_query_string = f'&q={search_term}'

    cart_products = ShoppingCart.objects.filter(
        client__user = request.user
    ).order_by('-id')

    user_profile = UserProfile.objects.filter(
        user=request.user
    ).first()

    page_object, pagination_range = make_pagination(request, services, PER_PAGE)

    products_amount = 0
    for cart_product in cart_products:
        products_amount += cart_product.amount

    context = {
        'additional_url_query': additional_query_string,
        'pagination_range': pagination_range,
        'products_amount': products_amount,
        'search_term': search_term,
        'services': page_object, 
        'user_profile': user_profile,
    }

    return render(request=request, template_name='main/pages/services.html', context=context)


@login_required(login_url='main_app:login', redirect_field_name='next')
def service(request, slug):

    cart_products = ShoppingCart.objects.filter(
        client__user = request.user
    ).order_by('-id')

    user_profile = UserProfile.objects.filter(
        user=request.user
    ).first()

    products_amount = 0
    for cart_product in cart_products:
        products_amount += cart_product.amount

    context = {
        'products_amount': products_amount,
        'user_profile': user_profile,
    }

    return render(request=request, template_name='main/pages/services.html', context=context)


@login_required(login_url='main_app:login', redirect_field_name='next')
def requests(request):

    cart_products = ShoppingCart.objects.filter(
        client__user = request.user
    ).order_by('-id')

    user_profile = UserProfile.objects.filter(
        user=request.user
    ).first()

    user_requests = Requests.objects.filter(
        owner=user_profile
    ).order_by('-id')    

    search_term = request.GET.get('q', '').strip()

    if user_profile.serviceTer != 'Nenhum':
        if not search_term:
            others_requests = Requests.objects.filter(
                ~Q(owner=user_profile),
                Q(concluded=False)
            ).order_by('-id')
            additional_query_string = ''
        else:
            others_requests = Requests.objects.filter(
                Q(name__icontains=search_term),
                ~Q(owner=user_profile),
                Q(concluded=False)
            ).order_by('-id')
            additional_query_string = f'&q={search_term}'
    
        page_object, pagination_range = make_pagination(request, others_requests, PER_PAGE)

    products_amount = 0
    for cart_product in cart_products:
        products_amount += cart_product.amount

    context = {
        'additional_query_string': additional_query_string,
        'pagination_range': pagination_range,
        'others_requests': page_object,
        'products_amount': products_amount,
        'user_profile': user_profile,
        'user_requests': user_requests,
    }

    return render(request=request, template_name='main/pages/requests.html', context=context)


@login_required(login_url='main_app:login', redirect_field_name='next')
def request(request, slug):

    cart_products = ShoppingCart.objects.filter(
        client__user = request.user
    ).order_by('-id')

    user_profile = UserProfile.objects.filter(
        user=request.user
    ).first()

    products_amount = 0
    for cart_product in cart_products:
        products_amount += cart_product.amount

    context = {
        'products_amount': products_amount,
        'user_profile': user_profile,
    }

    return render(request=request, template_name='main/pages/request.html', context=context)


@login_required(login_url='main_app:login', redirect_field_name='next')
def company(request, slug):
    company = get_object_or_404(
        Companies, slug=slug
    )

    products = Products.objects.filter(
        company__id=company.id
    ).order_by('-id')

    services = Services.objects.filter(
        company__id=company.id
    ).order_by('-id')

    social_medias = SocialMedia.objects.filter(
        company__id=company.id
    ).order_by('-id')

    cart_products = ShoppingCart.objects.filter(
        client__user = request.user
    ).order_by('-id')

    user_profile = UserProfile.objects.filter(
        user=request.user
    ).first()

    products_amount = 0
    for cart_product in cart_products:
        products_amount += cart_product.amount

    context = {
        'company': company, 
        'products': products,
        'products_amount': products_amount,
        'services': services,
        'social_medias': social_medias,
        'user_profile': user_profile,
    }

    return render(request=request, template_name='main/pages/company.html', context=context)


@login_required(login_url='main_app:login', redirect_field_name='next')
def profile(request, slug):

    profile = get_object_or_404(
        UserProfile, user__username=slug
    )

    user_profile = UserProfile.objects.filter(
        user=request.user
    ).first()

    cart_products = ShoppingCart.objects.filter(
        client__user = request.user
    ).order_by('-id')

    companies_owned = Companies.objects.filter(
        owner__CPF=profile.CPF
    )

    companies_working = Employee.objects.filter(
        employee__CPF=profile.CPF
    )

    products_amount = 0
    for cart_product in cart_products:
        products_amount += cart_product.amount

    context = {
        'companies_owned': companies_owned,
        'companies_working': companies_working,
        'products_amount': products_amount,
        'profile': profile,
        'user_profile': user_profile,
    }

    return render(request=request, template_name='main/pages/profile.html', context=context)


@login_required(login_url='main_app:login', redirect_field_name='next')
def dashboard(request):

    cart_products = ShoppingCart.objects.filter(
        client__user = request.user
    ).order_by('-id')

    user_profile = UserProfile.objects.filter(
        user=request.user
    ).first()

    user_companies = Companies.objects.filter(
        owner = user_profile
    ).order_by('-id')

    products_amount = 0
    for cart_product in cart_products:
        products_amount += cart_product.amount

    if user_profile.serviceTer == 'Nenhum':
        return redirect('main_app:home')

    context = {
        'products_amount': products_amount,
        'user_profile': user_profile,
        'user_companies': user_companies,
    }

    return render(request=request, template_name='main/pages/dashboard.html', context=context)


@login_required(login_url='main_app:login', redirect_field_name='next')
def register_company_view(request):

    cart_products = ShoppingCart.objects.filter(
        client__user = request.user
    ).order_by('-id')

    user_profile = UserProfile.objects.filter(
        user=request.user
    ).first()

    products_amount = 0
    for cart_product in cart_products:
        products_amount += cart_product.amount

    if user_profile.serviceTer == 'Nenhum':
        return redirect('main_app:home')

    company_form_data = request.session.get('company_form_data', None)
    form = RegisterCompanyForm(company_form_data)

    context = {
        'form': form,
        'products_amount': products_amount,
        'user_profile': user_profile,
    }

    return render(request=request, template_name='main/pages/register-company.html', context=context)


@login_required(login_url='main_app:login', redirect_field_name='next')
def register_company_create(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    FILES = request.FILES
    request.session['company_form_data'] = POST
    form = RegisterCompanyForm(POST, FILES)

    user_profile = UserProfile.objects.filter(
        user=request.user
    ).first()

    if user_profile.serviceTer == 'Nenhum':
        return redirect('main_app:home')

    if form.is_valid():
        form.save(user_profile)
        messages.success(request, 'Empresa criada com sucesso.')

        del(request.session['company_form_data'])
        return redirect('main_app:company_view')

    return redirect('main_app:dashboard')


@login_required(login_url='main_app:login', redirect_field_name='next')
def historic(request):

    cart_products = ShoppingCart.objects.filter(
        client__user = request.user
    ).order_by('-id')

    user_profile = UserProfile.objects.filter(
        user=request.user
    ).first()

    products_amount = 0
    for cart_product in cart_products:
        products_amount += cart_product.amount

    context = {
        'products_amount': products_amount,
        'user_profile': user_profile,
    }

    return render(request=request, template_name='main/pages/historic.html', context=context)


def register_view(request):
    sign_up_form_data = request.session.get('sign_up_form_data', None)
    form = SignUpForm(sign_up_form_data)

    context = {
        'form': form,
    }

    return render(request=request, template_name='main/pages/register.html', context=context)


def register_create(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['sign_up_form_data'] = POST
    form = SignUpForm(POST)

    if form.is_valid():
        form.save()
        messages.success(request, 'Cadastro efeituado com sucesso.')

        del(request.session['sign_up_form_data'])
        return redirect('main_app:login')

    return redirect('main_app:register')


def login_view(request):
    form = LoginForm()

    context = {
        'form': form,
    }

    return render(request=request, template_name='main/pages/login.html', context=context)


def login_validate(request):
    if not request.POST:
        raise Http404()

    form = LoginForm(request.POST)

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )

        if authenticated_user is not None:
            login(request, authenticated_user)
            return redirect('main_app:home')
        else:
            messages.error(request, 'Credenciais invalidas')
    else:
        messages.error(request, 'Credenciais invalidas saca')

    return redirect('main_app:login')


@login_required(login_url='main_app:login', redirect_field_name='next')
def logout_view(request):
    if request.POST:
        logout(request)
    
    return redirect('main_app:login')


@login_required(login_url='main_app:login', redirect_field_name='next')
def shopping_cart(request):
    
    cart_products = ShoppingCart.objects.filter(
        client__user = request.user
    ).order_by('-id')

    user_profile = UserProfile.objects.filter(
        user=request.user
    ).first()

    products_amount = 0
    products_value = 0
    for cart_product in cart_products:
        products_amount += cart_product.amount
        products_value += cart_product.finalPrice

    products_freight = 19.99

    products_final_value = float(products_value) + float(products_freight)

    context = {
        'cart_products': cart_products,
        'products_amount': products_amount,        
        'products_final_value': products_final_value,
        'products_freight': products_freight,
        'products_value': products_value,
        'user_profile': user_profile,
    }

    return render(request=request, template_name='main/pages/cart.html', context=context)


@login_required(login_url='main_app:login', redirect_field_name='next')
def shopping_delete(request):
    if request.method == 'POST':
        cart_item_id = request.POST.get('cart_item_id')
        existing_item = ShoppingCart.objects.filter(
            id=cart_item_id,
        ).first()
        if existing_item:
            existing_item.delete()
    else:
        raise Http404()

    return redirect('main_app:shopping')


@login_required(login_url='main_app:login', redirect_field_name='next')
def shopping_edit(request):
    if request.method == 'POST':
        cart_item_id = request.POST.get('cart_item_id')
        existing_item = ShoppingCart.objects.filter(
            id=cart_item_id,
        ).first()
        if existing_item:
            if request.POST.get('type') == 'raise':
                existing_item.amount += 1
                existing_item.save()
            if request.POST.get('type') == 'decrease':
                if existing_item.amount != 1:
                    existing_item.amount -= 1
                existing_item.save()
    else:
        raise Http404()

    return redirect('main_app:shopping')


@login_required(login_url='main_app:login', redirect_field_name='next')
def about_us(request):
    cart_products = ShoppingCart.objects.filter(
        client__user = request.user
    ).order_by('-id')

    user_profile = UserProfile.objects.filter(
        user=request.user
    ).first()

    products_amount = 0
    for cart_product in cart_products:
        products_amount += cart_product.amount


    context = {
        'products_amount': products_amount, 
        'user_profile': user_profile,
    }

    return render(request=request, template_name='main/pages/about-us.html', context=context)