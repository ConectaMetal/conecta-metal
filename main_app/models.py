from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Empresas(models.Model):
    CNPJ = models.CharField(max_length=14)
    razaoSocial = models.CharField(max_length=255)
    nomeFantasia = models.CharField(max_length=255)
    profilePic = models.ImageField(upload_to='main/prof_pics/%Y/%m/%d/')
    isValid = models.BooleanField(default=False)

