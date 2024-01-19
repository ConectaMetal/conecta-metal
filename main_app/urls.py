from django.urls import path
from . import views

app_name = 'main_app'

urlpatterns = [
    path('', views.home, name="home"),
    path('product/<slug:slug>/', views.product, name="product"),
    path('sign/', views.sign, name="sign")
]
