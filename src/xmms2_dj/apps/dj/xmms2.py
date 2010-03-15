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
            title_list += [(pl_id, info["artist"], info["title"])]
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
