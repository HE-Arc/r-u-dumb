from django import template

register = template.Library()

@register.filter(name='arrayElement')
def arrayElement(value, arg):
    """Removes all values of arg from the given string"""
    return value[arg]
