from django.shortcuts import render
from . import models

# Create your views here.
def home(request):
    return render(request=request, template_name='main/pages/home.html')