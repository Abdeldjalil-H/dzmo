from django import template

register = template.Library()

@register.filter
def ltr(is_ltr):
    if is_ltr:
        return 'dir=ltr style=text-align:left'
    return ''