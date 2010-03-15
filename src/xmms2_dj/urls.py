from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Alle Urls an dj weiterleiten
    (r'^', include('xmms2_dj.apps.dj.urls')),
)
