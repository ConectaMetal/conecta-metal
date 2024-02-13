import requests
from django import forms
from ..models import Companies
from django.core.exceptions import ValidationError
from utils import form_utils as fu


class RegisterForm(forms.ModelForm):

    repeatPassword = forms.CharField()

    class Meta:
        model = Companies
        fields = [
            'CNPJ', 'legalName', 'businessName', 'CEP', 'addressNumber', 'complement', 'phoneNumber', 'email', 'password', 'repeatPassword', 'description', 'profilePic', 'validatingDocument', 
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['CNPJ'].label = 'CNPJ'
        self.fields['CNPJ'].validators = [fu.valid_cnpj]
        self.fields['CNPJ'].widget.attrs['placeholder'] = 'CNPJ da empresa'

        self.fields['legalName'].label = 'Razão Social'
        self.fields['legalName'].widget.attrs['placeholder'] = 'Razão social'

        self.fields['businessName'].label = 'Nome Fantasia'
        self.fields['businessName'].widget.attrs['placeholder'] = 'Nome fantasia'

        self.fields['CEP'].label = 'CEP'
        self.fields['CEP'].validators = [fu.valid_cep]
        self.fields['CEP'].widget.attrs['placeholder'] = 'CEP da empresa'

        self.fields['addressNumber'].label = 'Endereço'
        self.fields['addressNumber'].widget.attrs['placeholder'] = 'Número do endereço'

        self.fields['complement'].label = 'Complemento'
        self.fields['complement'].widget.attrs['placeholder'] = 'Complemento'

        self.fields['phoneNumber'].label = 'Telefone'
        self.fields['phoneNumber'].widget.attrs['placeholder'] = 'Número para contato'

        self.fields['email'].label = 'E-mail'
        self.fields['email'].widget.attrs['placeholder'] = 'E-mail para contato'

        self.fields['password'].label = 'Senha'
        # self.fields['password'].validators = [fu.strong_password]
        self.fields['password'].widget = forms.PasswordInput()
        self.fields['password'].widget.attrs['placeholder'] = 'Sua senha'

        self.fields['repeatPassword'].label = 'Repetir Senha'
        self.fields['repeatPassword'].widget = forms.PasswordInput()
        self.fields['repeatPassword'].widget.attrs['placeholder'] = 'Repita sua senha'

        self.fields['description'].label = 'Descrição'
        self.fields['description'].widget.attrs['placeholder'] = 'Uma breve descrição da sua empresa'

        self.fields['profilePic'].label = 'Foto de Perfil'
        self.fields['profilePic'].error_messages = {'required': 'Esse campo é obrigatório.'}
        # The following line is for debugging
        self.fields['profilePic'].required = False

        self.fields['validatingDocument'].label = 'Documento Validador'
        self.fields['validatingDocument'].error_messages = {'required': 'Esse campo é obrigatório.'}
        # The following line is for debugging
        self.fields['validatingDocument'].required = False


    def clean_CNPJ(self):
        data = self.cleaned_data.get('CNPJ')
        url = f"https://publica.cnpj.ws/cnpj/{fu.clear_data(data)}"
        response = requests.get(url)

        if response.status_code != 200:
            raise ValidationError(
                'CNPJ inválido',
                code='invalid'
            )
        
        instance = super().save(commit=False)
        instance.registrationStatus = response.json()['estabelecimento']['situacao_cadastral']

        return fu.clear_data(data)
    
    def clean_CEP(self):
        data = self.cleaned_data.get('CEP')
        url = f'https://viacep.com.br/ws/{fu.clear_data(data)}/json/'
        response = requests.get(url)

        if response.status_code != 200:
            raise ValidationError('Tente novamente mais tarde')
        
        if 'erro' in response.json():
            raise ValidationError(
                'CEP inválido',
                code='invalid'
            )
        
        instance = super().save(commit=False)
        instance.state = response.json()['uf']
        instance.city = response.json()['localidade']
        instance.neigborhood = response.json()['bairro']
        instance.streetAddress = response.json()['logradouro']
            
        return fu.clear_data(data)
    
    def clean_email(self):
        data = self.cleaned_data.get('email')

        if Companies.objects.filter(email=data).exists():
            raise ValidationError(
                'E-mail já cadastrado',
                code='invalid'
            )
        
        return data
    
    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        repeat_password = cleaned_data.get('repeatPassword')

        if password != repeat_password:
            raise ValidationError({
                'password': 'As senhas não coincidem',
                'repeatPassword': 'As senhas não coincidem'
            })

        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)

        # Create the slug for the company
        legal_name = self.cleaned_data.get('legalName')
        instance.slug = fu.clear_text(legal_name).replace(' ', '_').lower()

        instance = super().save(commit=True)

