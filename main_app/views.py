from django.http.response import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from main_app.models import Products, Companies, SocialMedia
from utils.pagination import make_pagination
from .forms import RegisterForm, LoginForm, SignUpForm
from utils import form_utils as fu

import os

PER_PAGE = int(os.environ.get('PER_PAGE', 30))

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


def register_view(request):
    sign_up_form_data = request.session.get('sign_up_form_data', None)
    form = SignUpForm(sign_up_form_data)

    context = {
        'is_sign_page': True,
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
        'is_sign_page': True,
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