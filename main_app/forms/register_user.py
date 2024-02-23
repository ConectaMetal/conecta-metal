from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from ..models import UserProfile, Address
from utils import form_utils as fu
import requests


class SignUpForm(forms.Form):

    # Django User fields
    firstName = forms.CharField(
        label='Nome',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Ex.: Vitor Barbosa'
            }
        )
    )
    lastName = forms.CharField(
        label='Sobrenome',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Ex.: Nogueira'
            }
        )
    )
    username = forms.CharField(
        label='Usuário',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Como as pessoas verão seu nome'
            }
        )
    )
    email = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Ex.: email@email.com'
            }
        )
    )
    password1 = forms.CharField(
        label='Senha',
        validators = [fu.strong_password],
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Insira uma senha'
            }
        )
    )
    password2 = forms.CharField(
        label='Repetir senha',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Repita uma senha'
            }
        )
    )

    # Models UserProfile fields
    CPF = forms.CharField(
        label='CPF',
        validators = [fu.valid_cpf],
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Insira seu CPF'
            }
        )
    )

    # Models Address fields
    CEP = forms.CharField(
        label='CEP',
        validators = [fu.valid_cep],
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Insira seu CEP'
            }
        )
    )
    number = forms.CharField(
        label='Endereço',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Insira o número da loja ou residência'
            }
        )
    )
    complement = forms.CharField(
        label='Complemento',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Insira o complemento'
            }
        )
    )

    def clean_username(self):
        data = self.cleaned_data['username']

        if User.objects.filter(username=data).exists():
            raise ValidationError(
                'Usuário já cadastrado',
                code='invalid'
            )
        
        return data
    
    def clean_email(self):
        data = self.cleaned_data['email']

        if User.objects.filter(email=data).exists():
            raise ValidationError(
                'E-mail já cadastrado',
                code='invalid'
            )
        
        return data
    
    def clean_CPF(self):
        data = self.cleaned_data['CPF']
        data = fu.clear_data(data)

        if UserProfile.objects.filter(CPF=data).exists():
            raise ValidationError(
                'CPF já cadastrado',
                code='invalid'
            )
        
        return data
    
    def clean_CEP(self):
        data = self.cleaned_data['CEP']
        data = fu.clear_data(data)
        url = f'https://viacep.com.br/ws/{data}/json/'
        response = requests.get(url)

        if response.status_code != 200:
            raise ValidationError('Tente novamente mais tarde')
        
        if 'erro' in response.json():
            raise ValidationError(
                'CEP inválido',
                code='invalid'
            )

        return data

    def clean(self):
        cleaned_data = super().clean()

        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            raise ValidationError({
                'password1': 'As senhas não coincidem',
                'password2': 'As senhas não coincidem'
            })

        return cleaned_data
    
    def save(self):
        user = User.objects.create_user(
            first_name=self.cleaned_data['firstName'],
            last_name=self.cleaned_data['lastName'],
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1']
        )

        cep = self.cleaned_data['CEP']
        number = self.cleaned_data['number']
        complement = self.cleaned_data['complement']
        address = Address.objects.filter(
            CEP=cep,
            number=number,
            complement=complement
        ).first()

        if not address:
            url = f'https://viacep.com.br/ws/{cep}/json/'
            response = requests.get(url).json()

            address = Address.objects.create(
                CEP=cep,
                state=response['uf'],
                city=response['localidade'],
                neigborhood=response['bairro'],
                streetAddress=response['logradouro'],
                number=number,
                complement=complement
            )

        cpf = self.cleaned_data['CPF']
        profile = UserProfile.objects.create(
            user=user,
            CPF=cpf,
            address=address
        )

        return user, profile