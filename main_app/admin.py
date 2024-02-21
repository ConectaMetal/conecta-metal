from django.contrib import admin
from .models import Companies, Products, Requests, SocialMedia, Services, UserProfile, Employee, Address, ShoppingCart

# Register your models here.
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    ...

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    ...

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    ...

@admin.register(Companies)
class CompaniesAdmin(admin.ModelAdmin):
    ...

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    ...

@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    ...

@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    ...

@admin.register(Requests)
class RequestsAdmin(admin.ModelAdmin):
    ...

@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    ...

