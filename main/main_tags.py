from django import template

register = template.Library()

@register.simple_tag
def multiply_by_two(value):
    return float(value) * 2.0