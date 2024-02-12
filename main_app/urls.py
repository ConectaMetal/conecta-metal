from django.urls import path
from . import views

app_name = 'main_app'

urlpatterns = [
    path('', views.home, name="home"),
    path('product/<slug:slug>/', views.product, name="product"),
    path('company/<slug:slug>/', views.company, name="company"),
    path('register/', views.register_view, name="register"),
    path('register/create/', views.register_create, name="create"),
    path('login', views.login, name="login"),
]
