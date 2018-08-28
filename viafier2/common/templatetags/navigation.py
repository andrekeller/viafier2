from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag(takes_context=True)
def navactive(context, url, *args):
    request = context['request']
    if request.path.startswith(reverse(url, args=args)):
        return " class=active"
    return ""


@register.simple_tag(takes_context=True)
def navactive_exact(context, url, *args):
    request = context['request']
    if request.path == reverse(url, args=args):
        return " class=active"
    return ""
