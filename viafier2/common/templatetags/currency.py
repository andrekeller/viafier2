from django import template
from django.utils.translation import get_language
from django.utils.translation import to_locale
import locale

locale.setlocale(locale.LC_ALL, locale="{}.utf8".format(to_locale(get_language())))
register = template.Library()


@register.filter
def currency(value):
    if value is None:
        return None
    return locale.currency(value, grouping=True)