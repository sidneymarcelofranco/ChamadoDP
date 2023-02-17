from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def highlight_search(text, search):
    highlighted = text.replace(search, '<span class="fw-bold" style="background-color: yellow;">{}</span>'.format(search))
    return mark_safe(highlighted)