from django.contrib import admin
from .models import Companies, Products, SocialMedia

# Register your models here.
@admin.register(Companies)
class CompaniesAdmin(admin.ModelAdmin):
    ...

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    ...

@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    ...