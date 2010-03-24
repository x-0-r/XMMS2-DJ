# -*- coding: utf-8 -*-

from django import template

register = template.Library()

@register.filter
def minutes(value):
    """Gibt die Minuten eines Millisekundenwerts zurück"""
    return "%02d" % (int(value) / 60000)

@register.filter
def seconds(value):
    """Gibt die ganzen Sekunden eines Millisekundenwerts zurück"""
    return "%02d" % (( int(value) / 1000 ) % 60)

@register.filter
def timespan(value):
    """Gibt eine Zeispanne in Millisekunden als String formatiert zurück"""
    hours = int(value) / 3600000
    minutes = (int(value) % 3600000) / 60000
    seconds = (int(value) / 1000) % 60

    return "%02d:%02d:%02d" % (hours, minutes, seconds)

@register.filter
def datefromtimestamp(value, arg=None):
    """Formatiert einen Unix-Timestamp
    """
    from datetime import datetime
    from django.template.defaultfilters import date

    value = datetime.fromtimestamp(value)
    return date(value, arg)
