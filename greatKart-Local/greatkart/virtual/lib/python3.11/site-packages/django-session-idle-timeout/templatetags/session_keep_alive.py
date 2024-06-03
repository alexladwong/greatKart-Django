# -*- coding: UTF-8 -*-
from django import template
from django.conf import settings

register = template.Library()
@register.inclusion_tag('sessionidletimeout/js.html', takes_context=True)
def session_keep_alive(context):
    return context.update({
        'session_keepalive_interval': int(getattr(settings, 'SESSION_IDLE_TIMEOUT', 1800)) / 2 * 1000,
    })
