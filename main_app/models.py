from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Companies(models.Model):
    CNPJ = models.CharField(max_length=14)
    legalName = models.CharField(max_length=255)
    businessName = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    profilePic = models.ImageField(upload_to='main/prof_pics/%Y/%m/%d/')
    registrationStatus = models.CharField(max_length=100)
    CEP = models.CharField(max_length=10)
    address = models.CharField(max_length=255)
    phoneNumber = models.CharField(max_length=20, blank=True)
    email = models.CharField(max_length=255)
    rating = models.FloatField()
    validatingDocument = models.FileField()
    isPartner = models.BooleanField(default=False)
    isValid = models.BooleanField(default=False)

    def __str__(self):
        return self.legalName


class SocialMedia(models.Model):
    ...


class Products(models.Model):
    ...


class Services(models.Model):
    ...


class Invoice(models.Model):
    ...
