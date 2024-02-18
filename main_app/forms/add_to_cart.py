from django import forms
from ..models import ShoppingCart

class AddToCartForm(forms.ModelForm):
    
    class Meta:
        model = ShoppingCart
        fields = ("client", "product", "amount", "finalPrice")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)




