from django.contrib import admin
from .models import Companies, Products

# Register your models here.
@admin.register(Companies)
class CompaniesAdmin(admin.ModelAdmin):
    ...

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    ...