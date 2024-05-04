from django import template

register = template.Library()

@register.filter(name='format_stat')
def format_stat(name):
    return ' '.join(word.capitalize() for word in name.split('_'))

