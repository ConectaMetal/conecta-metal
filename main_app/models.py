from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from utils import models_utils as mu

# Create your models here.
class Address(models.Model):
    CEP = models.CharField(max_length=9)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    neigborhood = models.CharField(max_length=255)
    streetAddress = models.CharField(max_length=255)
    number = models.CharField(max_length=255)
    complement = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.CEP


class UserProfile(models.Model):
    class ServiceTierName(models.TextChoices):
        Nenhum = 'Nenhum', _('Nenhum')
        Bronze = 'Bronze', _('Bronze')
        Silver = 'Silver', _('Silver')
        Gold = 'Gold', _('Gold')
        Platinum = 'Platinum', _('Platinum')

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    CPF = models.CharField(max_length=14, unique=True)
    picture = models.ImageField(upload_to=mu.profile_image_upload, null=True, blank=True, default='/main/default/no_profile_picture.png')
    aboutMe = models.TextField(null=True, blank=True, default=None)
    phone = models.CharField(max_length=255, null=True, blank=True, default=None)
    serviceTer = models.CharField(
        max_length=8, choices=ServiceTierName.choices, default=ServiceTierName.Nenhum
    )
    address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.user.username
    
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)


class Companies(models.Model):
    CNPJ = models.CharField(max_length=50)
    legalName = models.CharField(max_length=255)
    businessName = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    profilePic = models.ImageField(upload_to=mu.company_image_upload)
    description = models.TextField(null=True, blank=True, default=None)
    owner = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, null=True, blank=True
    )
    address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, null=True, blank=True
    )
    isPartner = models.BooleanField(default=False)

    def __str__(self):
        return self.legalName

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)


class Employee(models.Model):
    employee = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, null=True, blank=True
    )
    company = models.ForeignKey(
        Companies, on_delete=models.CASCADE, null=True, blank=True
    )
    companyPosition = models.CharField(max_length=255)
    businessEmail = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.employee.user.username + ' - ' + self.company.legalName

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)


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
    mainPicture = models.ImageField(upload_to=mu.product_image_upload)
    secondPicture = models.ImageField(upload_to=mu.product_image_upload, null=True, blank=True)
    thirdPicture = models.ImageField(upload_to=mu.product_image_upload, null=True, blank=True)
    fourthPicture = models.ImageField(upload_to=mu.product_image_upload, null=True, blank=True)
    details = models.CharField(max_length=100)
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
    mainPicture = models.ImageField(upload_to=mu.service_image_upload)
    secondPicture = models.ImageField(upload_to=mu.service_image_upload, null=True, blank=True)
    thirdPicture = models.ImageField(upload_to=mu.service_image_upload, null=True, blank=True)
    details = models.CharField(max_length=255)
    description = models.TextField()
    rating = models.FloatField()
    company = models.ForeignKey(
        Companies, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.name


class Requests(models.Model):
    class RequestTypeName(models.TextChoices):
        Produto = 'Produto', _('Produto')
        Serviço = 'Serviço', _('Serviço')

    name = models.CharField(max_length=255)
    description = models.TextField()
    picture = models.ImageField(upload_to=mu.request_image_upload, null=True, blank=True)
    type = models.CharField(
        max_length=7, choices=RequestTypeName.choices, default=RequestTypeName.Serviço
    )
    maxBudget = models.DecimalField(max_digits=20, decimal_places=2)
    owner = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, null=True, blank=True
    )
    concluded = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)


class ShoppingCart(models.Model):
    client = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, null=True, blank=True
    )
    product = models.ForeignKey(
        Products, on_delete=models.CASCADE, null=True, blank=True
    )
    amount = models.IntegerField(default=1)
    finalPrice = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return self.product.name
    
    def save(self, *args, **kwargs):
        self.finalPrice = self.amount * self.product.value
        super(ShoppingCart, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)


class Invoice(models.Model):
    ...
