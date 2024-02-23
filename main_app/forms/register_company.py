import requests
from django import forms
from ..models import Companies, Address, UserProfile
from django.core.exceptions import ValidationError
from utils import form_utils as fu
import PIL


class RegisterCompanyForm(forms.Form):

    # Company Fields
    CNPJ = forms.CharField(
        label='CNPJ',
        validators=[fu.valid_cnpj],
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Ex.: "01.234.567/8910-11."'
            }
        )
    )
    legalName = forms.CharField(
        label='Razão Social',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Razão social da empresa'
            }
        )
    )
    businessName = forms.CharField(
        label='Nome Fantasia',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Nome fantasia da empresa'
            }
        )
    )

    # Address Fields
    CEP = forms.CharField(
        label='CEP',
        validators = [fu.valid_cep],
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Ex.: "12345-678"'
            }
        )
    )
    number = forms.IntegerField(
        label='Número',
        widget=forms.NumberInput(
            attrs={
                'placeholder': 'Número do endereço'
            }
        )
    )
    complement = forms.CharField(
        label='Complemento',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Complemento do endereço'
            }
        )
    )

    # More Company Fields
    description = forms.CharField(
        label='Descrição',
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Descrição da empresa'
            }
        )
    )
    profilePic = forms.ImageField(
        label='Foto de Perfil',
        required=False,
        widget=forms.FileInput()
    )

    def clean_CNPJ(self):
        data = self.cleaned_data.get('CNPJ')
        url = f"https://publica.cnpj.ws/cnpj/{fu.clear_data(data)}"
        response = requests.get(url)

        if response.status_code != 200:
            raise ValidationError(
                'CNPJ inválido',
                code='invalid'
            )

        return fu.clear_data(data)
    
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
    
    def save(self, user):
        cep = self.cleaned_data['CEP']
        number = str(self.cleaned_data['number'])
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

        cnpj = self.cleaned_data['CNPJ']
        legal_name = self.cleaned_data['legalName']
        business_name = self.cleaned_data['businessName']
        profile_pic = self.cleaned_data['profilePic']
        description = self.cleaned_data['description']
        
        company = Companies.objects.create(
            CNPJ=cnpj,
            legalName=legal_name,
            businessName=business_name,
            slug=fu.create_slug(legal_name),
            profilePic=profile_pic,
            description=description,
            owner=user,
            address=address,
            isPartner=True,
        )
        print('salvei')

        return company

