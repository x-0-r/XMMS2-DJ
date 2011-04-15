# -*- coding: utf-8 -*-

"""@package xmms2_dj.apps.dj.xmms2
Beinhaltet Helfer-Klassen für die Steuerung des XMMS2 Servers
"""

import xmmsclient
import xmmsclient.collections as coll
from xmmsclient import XMMSSync, XMMSError

import sys
import os 
class XmmsClient(object):
    """A wrapper to the xmmsclient
    """
    def __init__(self, name):
        self.client = XMMSSync(name)
        self.client.connect(os.getenv("XMMS_PATH"))

    def current(self):
        """return the currently played song
           
           @return songtitle or None (if nothing is played at the moment)
        """
        id = self.client.playback_current_id()
        if id == 0:
            return None
        info = self.client.medialib_get_info(id)
        if info != None:
            return (id, info["artist"], info["title"])
        else:
            return None
    
    def play(self):
        """start playback
        """
        self.client.playback_start()

    def pause(self):
        """pause playback
        """
        self.client.playback_pause()

    def stop(self):
        """stop playback
        """
        self.client.playback_stop()

    def prev(self):
        """Jump to previous playlist entry
        """
        self.client.playlist_set_next_rel(-1)
        self.client.playback_tickle()

    def next(self):
        """Jump to the next playlist entry
        """
        self.client.playlist_set_next_rel(1)
        self.client.playback_tickle()

    
    def jump(self, id):
        """jump to specified playlist entry

           @param id number of the playlist entry to jump to
        """
        self.client.playlist_set_next(id)
        self.client.playback_tickle()

    def list(self, with_mlibid=False):
        """list playlist entries

           @return an array of dicts for example:
               [{'id': 1, 'artist': 'Machine Head', 'title': Imperium', 'duration': 450000},]
        """
        id_list = self.client.playlist_list_entries()
        title_list = []
        pl_id = 0
        for id in id_list:
            info = self.client.medialib_get_info(id)
            entry = {'id': pl_id,
                            'artist': info.get("artist"),
                            'title': info.get("title"),
                            'duration': info.get("duration"),
                    }
            if with_mlibid:
                entry['mlibid'] = id
            title_list += [entry,]
            pl_id += 1

        return title_list
    
    def coll_query(self, keys, c = coll.Universe()):
        """Query a collection for media information
           
           @param keys list of keys which the result should include
           @return list of dicts
        """
        return self.client.coll_query_infos(c, keys)

    def playlist_add_id(self, id):
        """Add a medialib ID to the playlist"""
        return self.client.playlist_add_id(id)

    def playlist_add_collection(self, collection):
        """Add all entries in a collection to the playlist"""
        return self.client.playlist_add_collection(collection)

    def playlist_remove_id(self, id):
        """Remove an entry from the active playlist"""
        return self.client.playlist_remove_entry(id)

    def playlist_clear(self):
        """Remove all entries from the active playlist"""
        return self.client.playlist_clear()

    def playlist_list(self):
        """List all playlists"""
        result = self.client.playlist_list()
        list = []
        for entry in result:
            # by the xmms client conventions, lists starting with an underscore
            # may not be visible to users.
            if not entry.startswith('_'):
                list += [entry,]

        return list

    def playlist_active(self):
        """Return the name of the active playlist"""
        return self.client.playlist_current_active()

    def playlist_load(self, playlist):
        """Load the specified playlist
           
           @param playlist name of the playlist as string
        """
        return self.client.playlist_load(playlist)


    def playlist_create(self, playlist):
        """Create a ne playlist with the given name
           
           @param playlist name of the playlist
        """
        return self.client.playlist_create(playlist)

    def playlist_remove(self, playlist):
        """Löscht die aktuelle Playlist
        """
        return self.client.playlist_remove(playlist)

    def playlist_move(self, cur_pos, new_pos):
        """Move a playlist entry to a new position
           
           @param cur_pos the current position of the entry
           @param new_pos the new position of the entry
        """
        max_pos = len(self.list())-1
        if new_pos > max_pos or new_pos < 0 or cur_pos < 0 or cur_pos > max_pos:
            return False

        return self.client.playlist_move(cur_pos, new_pos)

    def playlist_shuffle(self):
        """Shuffle the active playlist
        """
        return self.client.playlist_shuffle()

    def get_info(self, id):
        """Return information on a title

           @param id title id
        """
        return self.client.medialib_get_info(id)

    def volume_up(self, vol_add, channel=None):
        """Rise volume
           
           @param vol_add Amount, the volume should be increased
           @param channel Channel <'left'|'right'> which should be modified

           @return <code>True</code> on success, otherwise <code>False</code>
        """
        volume = self.volume_get()
        # curr_vol wird als dict zurück gegeben, das die Lautstärke für die
        # Kanäle 'right' und 'left' enthält.
        # Falls keine Lautstärke ermittelt werden konnte, enthält es einen
        # String mit einer Fehlermeldung.
        if volume is None:
            return False

        if channel is None:
            for ch, value in volume.items():
                self.client.playback_volume_set(ch, value + vol_add)
        else:
            self.client.playback_volume_set(channel, volume[channel]+vol_add)

        return True

    def volume_down(self, vol_dec, channel=None):
        """Decrease volume

           @param vol_dec Amount, by which the volume should be decreased
           @param channel Channel <'left'|'right'> which should be modified

           @return <code>True</code> on success, otherwise <code>False</code>
        """
        volume = self.volume_get()
        # siehe volume_up(..)
        if volume is None:
            return False

        if channel is None:
            for ch, value in volume.items():
                self.client.playback_volume_set(ch, value - vol_dec)
        else:
            self.client.playback_volume_set(channel, volume[channel])

        return True

    def volume_get(self):
        """Get volume
        
           @return the current volume, for example
                   {'left': 100, 'right': 100}
        """
        try:
            volume = self.client.playback_volume_get()
        except XMMSError:
            volume = None

        return volume
