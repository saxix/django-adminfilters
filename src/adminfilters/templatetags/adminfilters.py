# -*- coding: utf-8 -*-
from django.template import Context, Library

register = Library()

ATTRIBUTE = '_filters_media'


@register.simple_tag(takes_context=True)
def filter_media(context, media):
    spec = context['spec']
    if not hasattr(spec.admin_site, ATTRIBUTE):
        setattr(spec.admin_site, ATTRIBUTE, [])
    processed = getattr(spec.admin_site, ATTRIBUTE)
    if spec.__class__ not in processed:
        processed.append(spec.__class__)
        return str(media)
    return ''
