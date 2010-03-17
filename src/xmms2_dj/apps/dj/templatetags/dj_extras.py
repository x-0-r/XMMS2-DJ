# -*- coding: utf-8 -*-

from django import template

register = template.Library()

@register.filter
def minutes(value):
    """Gibt die Minuten eines Millisekundenwerts zurück"""
    return int(value) / 60000

@register.filter
def seconds(value):
    """Gibt die ganzen Sekunden eines Millisekundenwerts zurück"""
    return ( int(value) / 1000 ) % 60

@register.filter
def timespan(value):
    """Gibt eine Zeispanne in Millisekunden als String formatiert zurück"""
    hours = int(value) / 3600000
    minutes = (int(value) % 3600000) / 60000
    seconds = (int(value) / 1000) % 60

    return "%s:%s:%s" % (hours, minutes, seconds)
