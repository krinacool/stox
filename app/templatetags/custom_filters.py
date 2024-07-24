import re
from django import template
from app.models import Instrument
register = template.Library()

@register.filter(name='insert_spaces')
def insert_spaces(text):
    if not isinstance(text, str):
        return text
    # Insert space before digits
    text_with_spaces = re.sub(r'(\D)(\d)', r'\1 \2', text)
    # Insert space after digits
    text_with_spaces = re.sub(r'(\d)(\D)', r'\1 \2', text_with_spaces)
    # Insert space between letters if they change from uppercase to lowercase or vice versa
    text_with_spaces = re.sub(r'([a-z])([A-Z])', r'\1 \2', text_with_spaces)
    text_with_spaces = re.sub(r'([A-Z])([a-z])', r'\1 \2', text_with_spaces)
    return text_with_spaces

@register.filter(name='company_name')
def company_name(symbol):
    if not isinstance(symbol, str):
        return symbol
    print(symbol)
    name = Instrument.objects.filter(tradingsymbol='SBIN').first().name
    return name
