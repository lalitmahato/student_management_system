from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

@register.filter(name='file_type')
def file_type(file_name):
    image = ['jpg', 'jpeg', 'png', 'gif', 'svg']
    document = ['doc', 'docx', 'pdf', 'txt', 'xls', 'xlsx', 'ppt', 'pptx']
    extension = file_name.split('.')[-1]
    if extension in image:
        return 'image'
    elif extension in document:
        return 'document'
    else:
        return 'other'