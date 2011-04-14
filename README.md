XMMS2-DJ
========

Watt is it?
-----------
XMMS2-DJ is a web client for the media player [XMMS2](http://xmms2.org). It is
based on the [Django](http://www.djangoproject.com) framework.

How does it work?
-----------------
To use XMMS2-DJ, you need a running http-server which can process python
scripts. For example Apache with mod_wsgi. For further information have a look
at the [Django
documentation](http://docs.djangoproject.com/en/dev/howto/deployment/).

Who needs something like this?
------------------------------
XMMS2-DJ is intended to run on a small home entertainment server. As a client on
a local computer it would be a bit of an overhead to run a web-server.

Installation
------------
Have a look at the [Django
documentation](http://docs.djangoproject.com/en/dev/howto/deployment/) on how to
deploy a django web application.
In order to have XMMS2-DJ working properly, you need to adjust the MEDIA_URL
constant in settings.py. It may also be necessary to adjust the XMMS_PATH in
apps/dj/xmms2.py around line 16.

Quick test
----------
For a quick test, start your xmms2 daemon,
	xmms2-launcher
mount the media files to where your MEDIA_URL points,
	mount --bind media/ /var/www/media
run the django development server.
	python manage.py runserver
