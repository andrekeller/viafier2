from django import template
from inventory.models import Article

register = template.Library()


@register.filter
def article_status_verbose(value):
    for id, status in Article.STATUS_CHOICES:
        if id == value:
            return status
