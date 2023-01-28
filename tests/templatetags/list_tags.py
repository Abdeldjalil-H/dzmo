from django import template

register = template.Library()


@register.filter
def index(sequence, position):
    return sequence[position]


@register.filter
def ltr(is_ltr):
    if is_ltr:
        return "dir=ltr style=text-align:left"
    return ""


@register.filter
def as_marks(marks):
    a = ["", "*", 0]
    return [x if x >= 0 else a[-x] for x in marks]
