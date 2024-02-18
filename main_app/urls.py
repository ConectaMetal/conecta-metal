from django.urls import path
from . import views

app_name = 'main_app'

urlpatterns = [
    path('', views.home, name="home"),
    path('product/<slug:slug>/', views.product, name="product"),
    path('service/', views.service, name="services"),
    path('service/<slug:slug>/', views.service, name="services"),
    path('company/<slug:slug>/', views.company, name="company"),
    path('shopping/', views.shopping_cart, name="shopping"),
    path('shopping/delete', views.shopping_delete, name="shopping_delete"),
    path('shopping/edit', views.shopping_edit, name="shopping_edit"),
    # Register / Login / Logout paths
    path('register/', views.register_view, name="register"),
    path('register/create/', views.register_create, name="create"),
    path('login/', views.login_view, name="login"),
    path('login/validate', views.login_validate, name='validate'),
    path('logout/', views.logout_view, name="logout")
]
