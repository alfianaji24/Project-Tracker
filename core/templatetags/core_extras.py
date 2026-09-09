from django import template

from core.utils import format_rupiah

register = template.Library()


@register.filter
def rupiah(value):
    return format_rupiah(value)
