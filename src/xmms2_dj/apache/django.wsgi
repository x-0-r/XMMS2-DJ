# -*- coding: utf-8 -*-

import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'xmms2_dj.settings'

sys.path.append('/srv/webapps')
sys.path.append('srv/webapps/xmms2_dj')
from django.core.handlers import wsgi

application = wsgi.WSGIHandler()

