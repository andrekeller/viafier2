from django import template
from django.conf import settings

register = template.Library()


@register.filter
def currency(value):
    if value is None:
        return None
    return "{} {:.2f}".format(
        settings.CURRENCY,
        value
    )
