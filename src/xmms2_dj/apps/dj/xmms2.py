# -*- coding: utf-8 -*-

"""@package xmms2_dj.apps.dj.xmms2
Beinhaltet Helfer-Klassen für die Steuerung des XMMS2 Servers
"""

import xmmsclient
import xmmsclient.collections as coll

import sys
import os

class XmmsClient(object):
    """Ein XMMS2 Client Wrapper
    """
    def __init__(self, name):
        self.client = xmmsclient.XMMS(name)
        self.client.connect(os.getenv("XMMS_PATH"))

    def current(self):
        """return the currently played song
           
           @return songtitle or None (if nothing is played at the moment)
        """
        result = self.client.playback_current_id()
        result.wait()
        id = result.value()
        if id == 0:
            return None
        result = self.client.medialib_get_info(id)
        result.wait()
        info = result.value()
        if info != None:
            return (id, info["artist"], info["title"])
        else:
            return None
    
    def play(self):
        """Playback starten
        """
        result = self.client.playback_start()
        result.wait()

    def stop(self):
        """Playback stoppen
        """
        result = self.client.playback_stop()
        result.wait()

    def prev(self):
        """Vorherigen Eintrag in Playlist abspielen
        """
        result = self.client.playlist_set_next_rel(-1)
        result.wait()
        result = self.client.playback_tickle()
        result.wait()

    def next(self):
        """Zum nächsten Eintrag in der Playlist springen
        """
        result = self.client.playlist_set_next_rel(1)
        result.wait()
        result = self.client.playback_tickle()
        result.wait()

    
    def jump(self, id):
        """Zu einem Eintrag in der Playlist springen
        """
        result = self.client.playlist_set_next(id)
        result.wait()
        result = self.client.playback_tickle()
        result.wait()

    def list(self):
        """Playlist auflisten

           @return ein Array aus Tupeln z.B.: [(1, 'Machine Head', 'Imperium'),]
        """
        result = self.client.playlist_list_entries()
        result.wait()
        id_list = result.value()
        title_list = []
        pl_id = 0
        for id in id_list:
            result = self.client.medialib_get_info(id)
            result.wait()
            info = result.value()
            title_list += [{'id': pl_id,
                            'artist': info["artist"],
                            'title': info["title"],
                            'duration': info["duration"],
                           }]
            pl_id += 1

        return title_list
    
    def coll_query(self, keys, c = coll.Universe()):
        """Eintraginfos aus einer Collection abrufen
        Dabei ist keys eine liste
        Zurückgegeben wird eine Liste mit dictionarys
        """
        result = self.client.coll_query_infos(c, keys)
        result.wait()
        return result.value()

    def playlist_add_id(self, id):
        """Eine Medialib-ID zur Playlist hinzufügen"""
        result = self.client.playlist_add_id(id)
        result.wait()
        return result.value()

    def playlist_add_collection(self, collection):
        """Alle Einträge einer Collection zur Playlist hinzufügen"""
        result = self.client.playlist_add_collection(collection)
        result.wait()
        return result.value()

    def playlist_remove_id(self, id):
        """Einen Eintrag aus der aktuellen Playlist entfernen"""
        result = self.client.playlist_remove_entry(id)
        result.wait()
        return result.value()

    def playlist_clear(self):
        """Die aktuelle Playlist leeren"""
        result = self.client.playlist_clear()
        result.wait()
        return result.value()

    def playlist_list(self):
        """Playlisten auflisten"""
        result = self.client.playlist_list()
        result.wait()
        list = []
        for entry in result.value():
            # laut Client-Konvention dürfen Listen, die mit '_' beginnen für
            # Benutzer nicht sichtbar sein
            if not entry.startswith('_'):
                list += [entry,]

        return list

    def playlist_active(self):
        """Gibt den Namen der aktiven Playlist zurück"""
        result = self.client.playlist_current_active()
        result.wait()
        return result.value()

    def playlist_load(self, playlist):
        """Lädt die angegebene Playliste"""
        result = self.client.playlist_load(playlist)
        result.wait()
        return result.value()


    def playlist_create(self, playlist):
        """Erstellt eine neue Playlist
           
           @param playlist Name der Playlist
        """
        result = self.client.playlist_create(playlist)
        result.wait()
        return result.value()

    def playlist_move(self, cur_pos, new_pos):
        """Einen Eintrag in der Playlist verschieben
           
           @param cur_pos Die aktuelle Position des Eintrags
           @param new_pos Die neue Position des Eintrags
        """
        max_pos = len(self.list())-1
        if new_pos > max_pos or new_pos < 0 or cur_pos < 0 or cur_pos > max_pos:
            print "Failed to move from %d to %d" % (cur_pos, new_pos)
            return False

        print "moving from %d to %d" % (cur_pos, new_pos)

        result = self.client.playlist_move(cur_pos, new_pos)
        result.wait()
        return result.value()
