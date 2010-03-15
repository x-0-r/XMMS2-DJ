# -*- coding: utf-8 -*-

"""@package xmms2_dj.apps.dj.views
"""

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import Context, loader, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.encoding import smart_str
from urllib import unquote_plus

import xmms2
from xmmsclient import collections

def common(request, client=settings.XMMS2_CLIENT, artist='Alle', album='Alle'):
    if artist != "Alle":
        artist_coll = collections.Match(field="artist", value=artist)
    else:
        artist_coll = collections.Universe()

    if album != "Alle":
        album_coll = collections.Intersection(
            artist_coll,
            collections.Match(field="album", value=album)
        )
    else:
        album_coll = collections.Intersection(
            artist_coll,
            collections.Universe()
        )

    template = loader.get_template('dj/index.html')
    context = RequestContext(request, {
        'playlist': client.list(),
        'current': client.current(),
        'artists': client.coll_query(['artist']),
        'selected_artist': artist,
        'albums': client.coll_query(['album'], artist_coll),
        'titles': client.coll_query(['id', 'title'], album_coll),
        })

    return HttpResponse(template.render(context))

def index(request):
    return common(request)    

def status(request):
    client = settings.XMMS2_CLIENT

    template = loader.get_template('dj/player_status.html')
    context = Context({
        'current': client.current(),
    })
    return HttpResponse(template.render(context))

def play(request):
    client = settings.XMMS2_CLIENT
    client.play()

    return status(request)

def stop(request):
    client = settings.XMMS2_CLIENT
    client.stop()

    return status(request)

def jump(request, id):

    id = int(id)

    client = settings.XMMS2_CLIENT
    client.jump(id)
    
    return status(request)

def next(request):
    client = settings.XMMS2_CLIENT
    client.next()

    return status(request)

def prev(request):
    client = settings.XMMS2_CLIENT
    client.prev()

    return status(request)


def artist_add(request, artist):
    client = settings.XMMS2_CLIENT

    artist = unquote_plus(artist)
    artist_coll = collections.Match(field="artist", value=artist)
    client.playlist_add_collection(artist_coll)

    template = loader.get_template('dj/playlist.html')
    context = RequestContext(request, {
        'playlist': client.list(),
    })
    return HttpResponse(template.render(context))


def album_add(request, artist, album):
    client = settings.XMMS2_CLIENT

    artist = unquote_plus(artist)
    album = unquote_plus(album)

    if artist != "Alle":
        artist_coll = collections.Match(field="artist", value=artist)
    else:
        artist_coll = collections.Universe()

    album_coll = collections.Intersection(
        artist_coll,
        collections.Match(field="album", value=album)
    )
    client.playlist_add_collection(album_coll)

    template = loader.get_template('dj/playlist.html')
    context = RequestContext(request, {
        'playlist': client.list(),
    })
    return HttpResponse(template.render(context))

def add_title(request, id):
    client = settings.XMMS2_CLIENT

    id = int(id)
    client.playlist_add_id(id)

    template = loader.get_template('dj/playlist.html')
    context = Context({
        'playlist': client.list(),
    })
    return HttpResponse(template.render(context))


def list_artists(requests):
    client = settings.XMMS2_CLIENT

    template = loader.get_template('dj/artistlist.html')
    context = Context({
        'artists': client.coll_query(['artist']),
    })

    return HttpResponse(template.render(context))


def list_albums(request, artist="Alle"):
    client = settings.XMMS2_CLIENT

    artist = unquote_plus(artist)

    artist = smart_str(artist) # vermeidet UnicodeError bei xmms2-Funktionen

    if artist != "Alle":
        artist_coll = collections.Match(field="artist", value=artist)
    else:
        artist_coll = collections.Universe()

    template = loader.get_template('dj/albumlist.html')
    context = RequestContext(request, {
        'selected_artist': artist,
        'albums': client.coll_query(['album'], artist_coll),
    })

    return HttpResponse(template.render(context))


def list_titles(request, artist="Alle", album="Alle"):
    client = settings.XMMS2_CLIENT

    artist = unquote_plus(artist)
    album = unquote_plus(album)

    print artist
    print album

    if artist != "Alle":
        artist_coll = collections.Match(field="artist", value=artist)
    else:
        artist_coll = collections.Universe()

    if album != "Alle":
        album_coll = collections.Intersection(
            artist_coll,
            collections.Match(field="album", value=album)
        )
    else:
        album_coll = collections.Intersection(
            artist_coll,
            collections.Universe()
        )

    print client.coll_query(['id', 'title'], album_coll)

    template = loader.get_template('dj/titlelist.html')
    context = RequestContext(request, {
        'selected_artist': artist,
        'albums': client.coll_query(['album'], artist_coll),
        'selected_album': album,
        'titles': client.coll_query(['id', 'title'], album_coll),
    })

    return HttpResponse(template.render(context))


def remove(request, id):
    id = int(id)
    client = settings.XMMS2_CLIENT
    client.playlist_remove_id(id)


    template = loader.get_template('dj/playlist.html')
    context = RequestContext(request, {
        'playlist': client.list(),
    })
    return HttpResponse(template.render(context))
