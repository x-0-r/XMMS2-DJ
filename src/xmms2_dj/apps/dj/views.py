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
    """Rendert die Index-Seite
    
    @deprecated wird nur noch von der Funktion index benötigt und kann daher in diese integriert werden
    """
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

    playlist = client.list()
    playtime = 0
    for entry in playlist:
        playtime += entry['duration']

    template = loader.get_template('dj/index.html')
    context = RequestContext(request, {
        'playlist': playlist,
        'playtime': playtime,
        'current': client.current(),
        'artists': client.coll_query(['artist']),
        'selected_artist': artist,
        'albums': client.coll_query(['album'], artist_coll),
        'titles': client.coll_query(['id', 'title'], album_coll),
        })

    return HttpResponse(template.render(context))


def index(request):
    """Rendert die Indexseite
    """
    return common(request)    


def status(request):
    """Updaten des Status des XMMS-Client
    """
    client = settings.XMMS2_CLIENT

    template = loader.get_template('dj/player_status.html')
    context = Context({
        'current': client.current(),
    })
    return HttpResponse(template.render(context))


def play(request):
    """Playback starten und Status updaten
    """
    client = settings.XMMS2_CLIENT
    client.play()

    return status(request)


def stop(request):
    """Playback stoppen und Status updaten
    """
    client = settings.XMMS2_CLIENT
    client.stop()

    return status(request)


def jump(request, id):
    """Zur Titel in Playlist springen und Status updaten
       
       @param id ID des Playlisteintrags
    """
    id = int(id)

    client = settings.XMMS2_CLIENT
    client.jump(id)
    
    return status(request)


def next(request):
    """Zu nächstem Eintrag in Playlist springen
    """
    client = settings.XMMS2_CLIENT
    client.next()

    return status(request)


def prev(request):
    """Zu vorherigem Eintrag in Playlist springen
    """
    client = settings.XMMS2_CLIENT
    client.prev()

    return status(request)

def get_playlist(request):
    """Liefert die aktuelle Playlist aus
    """
    client = settings.XMMS2_CLIENT

    playlist = client.list()
    playtime = 0
    for entry in playlist:
        playtime += entry['duration']

    template = loader.get_template('dj/playlist.html')
    context = RequestContext(request, {
        'playtime': playtime,
        'playlist': playlist,
    })
    return HttpResponse(template.render(context))


def artist_add(request, artist):
    """Alle Titel eines Künstlers zur Playlist hinzufügen
       
       @param artist Name des Künstlers (bzw. der Band)

       @remarks
         Evtl sollte Namensgebung nach "add_artist" geändert werden
    """
    client = settings.XMMS2_CLIENT

    artist = unquote_plus(artist)
    artist_coll = collections.Match(field="artist", value=artist)
    client.playlist_add_collection(artist_coll)

    return get_playlist(request)
    

def album_add(request, artist, album):
    """Alle Titel eines Albums zur Playlist hinzufügen

       @param artist Name des Künstlers
       @param album Albumname

       @remarks
         Name sollte evtl. nach "add_album" geändert werden
    """
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

    return get_playlist(request)

def add_title(request, id):
    """Einen Titel zur Playlist hinzufügen

       @param id ID des Titels (laut XMMS2 MediaLib)
    """
    client = settings.XMMS2_CLIENT

    id = int(id)
    client.playlist_add_id(id)

    return get_playlist(request)


def list_artists(requests):
    """Alle Künstler auflisten
    """
    client = settings.XMMS2_CLIENT

    template = loader.get_template('dj/artistlist.html')
    context = Context({
        'artists': client.coll_query(['artist']),
    })

    return HttpResponse(template.render(context))


def list_albums(request, artist="Alle"):
    """Alle Albem eines Künstlers auflisten
       
       @param artist Name des Künstlers/der Band
    """
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
    """Alle Titel eines Künstlers und oder eines Albums auflisten

       @param artist Name des Künstlers
       @param album Albumtitel
    """
    client = settings.XMMS2_CLIENT

    artist = smart_str(unquote_plus(artist)) # Vermeiden von UnicodeError
    album = smart_str(unquote_plus(album))

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

    template = loader.get_template('dj/titlelist.html')
    context = RequestContext(request, {
        'selected_artist': artist,
        'albums': client.coll_query(['album'], artist_coll),
        'selected_album': album,
        'titles': client.coll_query(['id', 'title'], album_coll),
    })

    return HttpResponse(template.render(context))


def remove(request, id):
    """Eintrag aus der aktiven Playlist entfernen
       
       @param id ID des Titels (entspricht Position in der Playlist)
    """
    id = int(id)
    client = settings.XMMS2_CLIENT
    client.playlist_remove_id(id)

    return get_playlist(request)
