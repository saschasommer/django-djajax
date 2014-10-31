# -*- coding: utf-8 -*-
"""
If the default usage of the views suits you, simply use a line like
this one in your root URLconf to set up the default URLs::

    (r'^messages/', include('djajax.urls')),

"""
from __future__ import unicode_literals

from django.conf.urls import patterns, url


urlpatterns = patterns(1, None, False, 'djajax.views',
                           
    url(r'^taggable_object/update/$', 'djajax_endpoint', name='taggable-object-update-api'),
                           
)
