from django import template
from django.utils.safestring import mark_safe
import mistune

register = template.Library()


@register.filter
def markdown(value):
    if value is None:
        return None
    parser = mistune.Markdown()
    return mark_safe(f'<div class="markdown">{parser(value)}</div>')
