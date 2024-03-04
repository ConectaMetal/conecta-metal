def product_image_upload(instance, filename):
    company_name = instance.company.legalName
    product_name = instance.name
    path = f'main/companies/{company_name}/products/{product_name}/{filename}'
    
    return path


def service_image_upload(instance, filename):
    company_name = instance.company.legalName
    service_name = instance.name
    path = f'main/companies/{company_name}/services/{service_name}/{filename}'
    
    return path


def request_image_upload(instance, filename):
    username = instance.owner
    request_name = instance.name
    path = f'main/users/{username}/requests/{request_name}/{filename}'
    
    return path


def company_image_upload(instance, filename):
    company_name = instance.legalName
    path = f'main/companies/{company_name}/picutre/{filename}'
    
    return path


def profile_image_upload(instance, filename):
    username = instance.user.username
    path = f'main/users/{username}/picture/{filename}'
    
    return path