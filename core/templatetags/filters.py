from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.simple_tag
def setvar(val=None):
    return val


@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)