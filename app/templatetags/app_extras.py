# In your_app/templatetags/your_app_extras.py
from django import template

register = template.Library()

@register.filter(name='multiply')
def multiply(value, arg):
    return value * arg

