# myapp/templatetags/custom_filters.py
from django import template
import time

register = template.Library()

@register.filter
def custom_function(a):
    return a

def ro(a):
    return round(a,2)
