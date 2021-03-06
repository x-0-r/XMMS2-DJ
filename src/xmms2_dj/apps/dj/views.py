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
    """Render the index page
    
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
        try:
            playtime += entry.get('duration')
        except TypeError:
            pass

    template = loader.get_template('concept/index.html')
    context = RequestContext(request, {
        'playlist_list': client.playlist_list(),
        'active_playlist': client.playlist_active(),
        'playlist': playlist,
        'playtime': playtime,
        'current': client.current(),
        'artists': client.coll_query(['artist']),
        'selected_artist': artist,
        'albums': client.coll_query(['album'], artist_coll),
        'titles': client.coll_query(['id', 'title'], album_coll),
        })

    return HttpResponse(template.render(context))


def index(request, client=settings.XMMS2_CLIENT):
    """Render the index page
    """
    if request.is_ajax():
        template = loader.get_template('concept/ajax/index.html')
        context = Context({
            'artists': client.coll_query(['artist',], collections.Universe()),
        })
        return HttpResponse(template.render(context))
    else:
        return common(request)    


def status(request, client=settings.XMMS2_CLIENT):
    """Updaten des Status des XMMS-Client
    """
    template = loader.get_template('dj/player_status.html')
    context = Context({
        'current': client.current(),
        'volume': client.volume_get(),
    })
    return HttpResponse(template.render(context))


def play(request, client = settings.XMMS2_CLIENT):
    """Playback starten und Status updaten
    """
    client.play()

    return status(request)


def pause(request, client = settings.XMMS2_CLIENT):
    """Playback pausieren und Status updaten
    """
    client.pause()

    return status(request)

def stop(request, client = settings.XMMS2_CLIENT):
    """Playback stoppen und Status updaten
    """
    client.stop()

    return status(request)


def jump(request, id, client = settings.XMMS2_CLIENT):
    """Zur Titel in Playlist springen und Status updaten
       
       @param id ID des Playlisteintrags
    """
    id = int(id)
    client.jump(id)
    
    return status(request)


def next(request, client = settings.XMMS2_CLIENT):
    """Zu nächstem Eintrag in Playlist springen
    """
    client.next()

    return status(request)


def prev(request, client = settings.XMMS2_CLIENT):
    """Zu vorherigem Eintrag in Playlist springen
    """
    client.prev()

    return status(request)


def get_playlist(request, client = settings.XMMS2_CLIENT):
    """Liefert die aktuelle Playlist aus
    """
    playlist = client.list()
    playtime = 0
    for entry in playlist:
        try:
            playtime += entry.get('duration')
        except TypeError:
            pass

    template = loader.get_template('concept/playlist.html')
    context = RequestContext(request, {
        'playtime': playtime,
        'playlist': playlist,
    })
    return HttpResponse(template.render(context))


def export_playlist(request, client = settings.XMMS2_CLIENT):
    """XML Export der Playlist
    """
    playlist = client.list(with_mlibid=True)
    template = loader.get_template('dj/playlist.xml')
    context = RequestContext(request, {
        'playlist': playlist,
    })
    return HttpResponse(template.render(context), mimetype='text/xml')

def artist_add(request, artist, client = settings.XMMS2_CLIENT):
    """Alle Titel eines Künstlers zur Playlist hinzufügen
       
       @param artist Name des Künstlers (bzw. der Band)

       @remarks
         Evtl sollte Namensgebung nach "add_artist" geändert werden
    """
    artist = unquote_plus(artist)
    artist_coll = collections.Match(field="artist", value=artist)
    client.playlist_add_collection(artist_coll)

    return get_playlist(request)
    

def album_add(request, artist, album, client = settings.XMMS2_CLIENT):
    """Alle Titel eines Albums zur Playlist hinzufügen

       @param artist Name des Künstlers
       @param album Albumname

       @remarks
         Name sollte evtl. nach "add_album" geändert werden
    """
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

def add_title(request, id, client = settings.XMMS2_CLIENT):
    """Einen Titel zur Playlist hinzufügen

       @param id ID des Titels (laut XMMS2 MediaLib)
    """
    id = int(id)
    client.playlist_add_id(id)

    return get_playlist(request)


def list_artists(requests, client = settings.XMMS2_CLIENT):
    """Alle Künstler auflisten
    """
    template = loader.get_template('dj/artistlist.html')
    context = Context({
        'artists': client.coll_query(['artist']),
    })

    return HttpResponse(template.render(context))


def list_albums(request, artist="Alle", client = settings.XMMS2_CLIENT):
    """Alle Albem eines Künstlers auflisten
       
       @param artist Name des Künstlers/der Band
    """
    artist = unquote_plus(artist)
    artist = smart_str(artist) # vermeidet UnicodeError bei xmms2-Funktionen

    if artist != "Alle":
        artist_coll = collections.Match(field="artist", value=artist)
    else:
        artist_coll = collections.Universe()

    template = loader.get_template('concept/albumlist.html')
    context = RequestContext(request, {
        'selected_artist': artist,
        'albums': client.coll_query(['album'], artist_coll),
    })

    return HttpResponse(template.render(context))


def list_titles(request, artist="Alle", album="Alle", client = settings.XMMS2_CLIENT):
    """Alle Titel eines Künstlers und oder eines Albums auflisten

       @param artist Name des Künstlers
       @param album Albumtitel
    """
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

    template = loader.get_template('concept/titlelist.html')
    context = RequestContext(request, {
        'selected_artist': artist,
        'albums': client.coll_query(['album'], artist_coll),
        'selected_album': album,
        'titles': client.coll_query(['id', 'title'], album_coll),
    })

    return HttpResponse(template.render(context))


def remove(request, id, client = settings.XMMS2_CLIENT):
    """Eintrag aus der aktiven Playlist entfernen
       
       @param id ID des Titels (entspricht Position in der Playlist)
    """
    id = int(id)
    client.playlist_remove_id(id)

    return get_playlist(request)


def clear_playlist(request, client = settings.XMMS2_CLIENT):
    """Die aktuelle Playliste leeren
    """
    client.playlist_clear()

    return get_playlist(request)


def load_playlist(request, playlist, client = settings.XMMS2_CLIENT):
    """Lädt eine Playlist
       
       @playlist Name der Playlist
    """
    playlist = smart_str(unquote_plus(playlist))
    client.playlist_load(playlist)

    return get_playlist(request)


def create_playlist(request, client = settings.XMMS2_CLIENT):
    """Erstelle eine neue Playlist"""
    playlist = request.POST.get("playlist")

    client.playlist_create(playlist)
    client.playlist_load(playlist)
    
    return get_playlist(request)

def remove_playlist(request):
    """Playlist entfernen"""
    client = settings.XMMS2_CLIENT

    playlist = request.POST.get('playlist')
    if playlist is None:
        playlist = client.playlist_active();
        client.playlist_load( client.playlist_list()[0] )
        # TODO error checking here!

    client.playlist_remove(playlist)
    
    return get_playlist(request)

def get_playlist_list(request, client = settings.XMMS2_CLIENT):
    """Rendert eine Liste vorhandener Playlists
    """
    template = loader.get_template("concept/playlist_list.html")
    context = Context({
        'playlist_list': client.playlist_list(),
        'active_playlist': client.playlist_active(),
    })
    return HttpResponse(template.render(context))


def search(request, client = settings.XMMS2_CLIENT):
    """Universelle Suche mit post-Daten
    """
    search = request.POST.get('search')
    search_type = request.POST.get('search-type')
    search = "*%s*" % search

    if search_type is None or search_type == 'all':
        coll = collections.Union(
            collections.Match(field="artist", value=search),
            collections.Match(field="album", value=search),
            collections.Match(field="title", value=search)
        )
    elif search_type == 'album':
        coll = collections.Union(
            collections.Match(field="album", value=search),
        )
    elif search_type == 'artist':
        coll = collections.Union(
            collections.Match(field="artist", value=search),
        )
    elif search_type == 'title':
        coll = collections.Union(
            collections.Match(field="title", value=search)
        )

    d = client.coll_query(['artist', 'album', 'title', 'id'], coll)
    t = {}
    for entry in d:
        if not entry['artist'] in t:
            t[entry['artist']] = {}
        if not entry['album'] in t[entry['artist']]:
            t[entry['artist']][entry['album']] = {}
        if not entry['title'] in t[entry['artist']][entry['album']]:
            t[entry['artist']][entry['album']][entry['title']] = entry['id']

    template = loader.get_template("concept/searchresult.html")
    context = RequestContext(request, {
        'result': t,
    })
    return HttpResponse(template.render(context))


def search_artist(request, client = settings.XMMS2_CLIENT):
    """Nach Künstler suchen

       @deprecated
    """
    artist = request.POST.get('artist')
    artist = "*%s*" % artist
    artist_coll = collections.Match(field="artist", value=artist)

    template = loader.get_template("dj/artistlist.html")
    context = Context({
        'artists': client.coll_query(['artist'], artist_coll),
    })
    return HttpResponse(template.render(context))


def search_album(request, client = settings.XMMS2_CLIENT):
    """Nach Album suchen

       @deprecated
    """
    artist = request.POST.get('artist')
    album = request.POST.get('album')
    album = "*%s*" % album
    album_coll = collections.Match(field="album", value=album)

    template = loader.get_template("dj/albumlist.html")
    context = Context({
        'selected_artist': artist,
        'albums': client.coll_query(['album'], album_coll),
    })
    return HttpResponse(template.render(context))


def search_title(request, client = settings.XMMS2_CLIENT):
    """Nach Titel suchen

       @deprecated
    """
    title = request.POST.get('title')
    title = "*%s*" % title
    title_coll = collections.Match(field="title", value=title)

    template = loader.get_template("dj/titlelist.html")
    context = Context({
        'titles': client.coll_query(['title', 'id'], title_coll),
    })
    return HttpResponse(template.render(context))


def shuffle_playlist(request, client = settings.XMMS2_CLIENT):
    """Die Playlist shufflen
    """
    client.playlist_shuffle()

    return get_playlist(request)


def move_entry(request, client = settings.XMMS2_CLIENT):
    """Einen Eintrag in der Playlist verschieben
    """
    old_pos = int(request.POST.get('old_pos'))
    new_pos = int(request.POST.get('new_pos'))
    
    res = client.playlist_move(old_pos, new_pos)

    if request.is_ajax():
        if res is None:
            return HttpResponse('True')
        else:
            return HttpResponse('False')
    else:
        return get_playlist(request)


def move_entry_down(request, pos, client = settings.XMMS2_CLIENT):
    """Einen Eintrag in der Playlist nach unten schieben

       @param pos Positon des Eintrags in der Playlist
    """
    pos = int(pos)
    client.playlist_move(pos, pos+1)

    return get_playlist(request)


def move_entry_up(request, pos, client = settings.XMMS2_CLIENT):
    """Einen Eintrag in der Playlist nach oben schieben

       @param pos Position des Eintrags in der Playlist
    """
    pos = int(pos)
    client.playlist_move(pos, pos-1)

    return get_playlist(request)


def show_info(request, id, client = settings.XMMS2_CLIENT):
    """Detailinfos über einen Song anzeigen

       @param id ID des Songs
    """
    id = int(id)

    template = loader.get_template("dj/titleinfo.html")
    context = RequestContext(request, {
        'infos': client.get_info(id),
    })
    return HttpResponse(template.render(context))


def volume_down(request, vol_add, client = settings.XMMS2_CLIENT):
    """Lautsärke verringern"""
    vol_dec = int(vol_add)
    
    if client.volume_down(vol_dec):
        volume = client.volume_get()
    else:
        volume = 'False'

    if request.is_ajax():
        return HttpResponse(volume);

    return HttpResponse("volume")
    
def volume_up(request, vol_add, client = settings.XMMS2_CLIENT):
    """Lautstärke erhöhen"""
    vol_add = int(vol_add)

    if client.volume_up(vol_add):
        volume = client.volume_get()
    else:
        volume = 'False'

    if request.is_ajax():
        return HttpResponse(volume);

    return HttpResponse("volume")
