# -*- coding: utf-8 -*-

from django.conf import settings
from django.utils.encoding import force_unicode

from xmmsclient import collections as coll

class DoesNotExist(Exception):
    pass

class MultipleObjectsReturned(Exception):
    pass

class Song(object):
    """Representing a song in the XMMS2 media libraray
    """
    client = settings.XMMS2_CLIENT

    def __init__(self, id=None, artist=None, album=None, title=None):
        self.id = id
        self.artist = artist
        self.album = album
        self.title = title


    @classmethod
    def get_from_dict(cls, data):
        """Create a new instance filled with data from a dict

           prevents "TypeError: __init__() got an unexpected keyword argument"
           when using x = Song(**data)
        """
        s = cls()
        for x in data:
            if x in s.__dict__:
                s.__dict__[x] = data[x]
        return s

    @classmethod
    def get(cls, **kwargs):
        """Search for a song in the media library
        """
        c = None
        for x in kwargs:
            if c:
                c = coll.Intersection(
                    c,
                    coll.Match(field=x, value=force_unicode(kwargs[x])) # xmmsclient expects both args to be str or unicode
                )
            else:
                c = coll.Match(field=x, value=force_unicode(kwargs[x]))
        result = cls.client.coll_query(['id', 'artist', 'title'], c)
        num = len(result)
        if num == 1:
            return cls.get_from_dict(result[0])
        if not num:
            raise DoesNotExist("Song matching query does not exist.")
        raise MultipleObjectsReturned("get() returned more than one Items! Lookup parameters were %s" % kwargs)
