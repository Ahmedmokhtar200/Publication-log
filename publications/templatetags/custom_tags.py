from django import template

register = template.Library()

counter = 1


@register.simple_tag()
def count_email(counter):
    counter = + 1
    return counter
