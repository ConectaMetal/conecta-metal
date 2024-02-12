from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Companies(models.Model):
    CNPJ = models.CharField(max_length=50)
    legalName = models.CharField(max_length=255)
    businessName = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    profilePic = models.ImageField(upload_to='main/prof_pics/%Y/%m/%d/')
    description = models.TextField(null=True, blank=True, default=None)
    registrationStatus = models.CharField(max_length=100)
    CEP = models.CharField(max_length=10)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    neigborhood = models.CharField(max_length=255)
    streetAddress = models.CharField(max_length=255)
    addressNumber = models.CharField(max_length=255)
    complement = models.CharField(max_length=100, blank=True)
    phoneNumber = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=255)
    validatingDocument = models.FileField()
    isPartner = models.BooleanField(default=False)
    isValid = models.BooleanField(default=False)

    def __str__(self):
        return self.legalName


class SocialMedia(models.Model):

    class SocialMediaName(models.TextChoices):
        WhatsApp = 'WhatsApp', _('Whatsapp')
        Instagram = 'Instagram', _('Instagram')
        Facebook = 'Facebook', _('Facebook')
        TikTok = 'TikTok', _('TikTok')
        Telegram = 'Telegram', _('Telegram')
        Kwai = 'Kwai', _('Kwai')
        Twitter = 'Twitter', _('Twitter')
        Pinterest = 'Pinterest', _('Pinterest')
        LinkedIn = 'LinkedIn', _('LinkedIn')
        Snapchat = 'Snapchat', _('Snapchat')

    name = models.CharField(
        max_length=9, choices=SocialMediaName.choices, default=SocialMediaName.Instagram
    )
    icon = models.TextField(blank=True, null=True)
    link = models.CharField(max_length=255)
    company = models.ForeignKey(
        Companies, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.name


class Products(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    mainPicture = models.ImageField(upload_to='main/products/%Y/%m/%d/')
    secondPicture = models.ImageField(upload_to='main/products/%Y/%m/%d/', null=True, blank=True)
    thirdPicture = models.ImageField(upload_to='main/products/%Y/%m/%d/', null=True, blank=True)
    fourthPicture = models.ImageField(upload_to='main/products/%Y/%m/%d/', null=True, blank=True)
    details = models.CharField(max_length=255)
    description = models.TextField()
    value = models.DecimalField(max_digits=20, decimal_places=2)
    stock = models.DecimalField(max_digits=20, decimal_places=2)
    rating = models.FloatField()
    company = models.ForeignKey(
        Companies, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.name


class Services(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    mainPicture = models.ImageField(upload_to='main/services/%Y/%m/%d/')
    secondPicture = models.ImageField(upload_to='main/services/%Y/%m/%d/', null=True, blank=True)
    thirdPicture = models.ImageField(upload_to='main/services/%Y/%m/%d/', null=True, blank=True)
    details = models.CharField(max_length=255)
    description = models.TextField()
    rating = models.FloatField()
    company = models.ForeignKey(
        Companies, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.name


class BuyCart(models.Model):
    customer = models.ForeignKey(
        Companies, on_delete=models.SET_NULL, null=True, blank=True
    )
    product = models.ForeignKey(
        Products, on_delete=models.SET_NULL, null=True, blank=True
    )
    amount = models.DecimalField(max_digits=20, decimal_places=5)

    def __str__(self):
        return self.product


class Invoice(models.Model):
    ...
