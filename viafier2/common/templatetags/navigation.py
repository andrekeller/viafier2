from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag(takes_context=True)
def navactive(context, url):
    request = context['request']
    if request.path.startswith(reverse(url)):
        return " class=active"
    return ""
