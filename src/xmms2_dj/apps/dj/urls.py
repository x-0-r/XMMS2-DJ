from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name="dj_index"),
                       url(r'^status/$', views.status, name="dj_status"),
                       url(r'^jump/(?P<id>\d+)/$', views.jump, name="dj_jump"),
                       url(r'^next/$', views.next, name="dj_next"),
                       url(r'^prev/$', views.prev, name="dj_previous"),
                       url(r'^play/$', views.play, name="dj_play"),
                       url(r'^stop/$', views.stop, name="dj_stop"),
                       #url(r'^artist/(?P<artist>.*)/$', views.artist_select, name="dj_artist_select"),
                       #url(r'^album/(?P<artist>.*)/(?P<album>.*)/$', views.album_select
                       url(r'^artists/$', views.list_artists, name="dj_list_artists"),
                       url(r'^albums/(?P<artist>.*)/$', views.list_albums, name="dj_list_albums"),
                       url(r'^titles/(?P<artist>.*)/(?P<album>.*)/$', views.list_titles, name="dj_list_titles"),
                       url(r'^add/artist/(?P<artist>.*)/$', views.artist_add, name="dj_add_artist"),
                       url(r'^add/album/(?P<artist>.*)/(?P<album>.*)/$', views.album_add, name="dj_add_album"),
                       url(r'^remove/(?P<id>\d+)/$', views.remove, name="dj_remove")
                      )
