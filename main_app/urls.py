from django.urls import path
from . import views

app_name = 'main_app'

urlpatterns = [
    # Main paths
    path('', views.home, name="home"),
    path('product/<slug:slug>/', views.product, name="product"),
    path('service/', views.services, name="services"),
    path('service/<slug:slug>/', views.service, name="service"),
    path('requests/', views.requests, name="requests"),
    path('requests/<slug:slug>', views.request, name="request"),

    # Company Register Paths
    path('dashboard/company/', views.register_company_view, name="company_view"),
    path('dashboard/company/create', views.register_company_create, name="company_create"),

    # Profile paths
    path('company/<slug:slug>/', views.company, name="company"),
    path('profile/<slug:slug>/', views.profile, name="profile"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('historic/', views.historic, name="historic"),

    # Shopping Cart paths
    path('shopping/', views.shopping_cart, name="shopping"),
    path('shopping/delete', views.shopping_delete, name="shopping_delete"),
    path('shopping/edit', views.shopping_edit, name="shopping_edit"),
    
    # Register / Login / Logout paths
    path('register/', views.register_view, name="register"),
    path('register/create/', views.register_create, name="create"),
    path('login/', views.login_view, name="login"),
    path('login/validate', views.login_validate, name='validate'),
    path('logout/', views.logout_view, name="logout"),

    # Other paths
    path('about/', views.about_us, name="about"),
]
