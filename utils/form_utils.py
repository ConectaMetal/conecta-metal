from django.core.exceptions import ValidationError
from validate_docbr import CPF
import re


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')
    if not regex.match(password):
        raise ValidationError(
            'Senha muito fraca',
        )
    

def clear_text(text):
    new_text = ''.join(e for e in text if e.isalnum() or e.isspace())
    new_text = ' '.join(new_text.split())
    return new_text


def create_slug(text):
    slug = text.strip()
    slug = "_".join(slug.split())
    slug = slug.lower()
    return slug


def clear_data(data):
    data = re.sub(r'[^a-zA-Z0-9]', ' ', data)
    clear_data = ''.join(data.split())
    return clear_data


def valid_cnpj(cnpj):
    clear_cnpj = clear_data(cnpj)
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])$')
    if regex.match(clear_cnpj):
        raise ValidationError('CNPJ inválido')
    
    regex = re.compile(r'^(?=.*[0-9]).{14,14}$')
    if not regex.match(clear_cnpj):
        raise ValidationError('CNPJ inválido')
    
    
def valid_cep(cep):
    clear_cep = clear_data(cep)
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])$')
    if regex.match(clear_cep):
        raise ValidationError('CEP inválido')
    
    regex = re.compile(r'^(?=.*[0-9]).{8,8}$')
    if not regex.match(clear_cep):
        raise ValidationError('CEP inválido')
    

def valid_cpf(cpf):
    cpf_validador = CPF()

    if not cpf_validador.validate(cpf):
        raise ValidationError('CPF inválido')
    
