# -*- coding: utf-8 -*-
"""
If the default usage of the views suits you, simply use a line like
this one in your root URLconf to set up the default URLs::

    (r'^messages/', include('djajax.urls')),

"""
from __future__ import unicode_literals

from django.conf.urls import url
from djajax import views

urlpatterns = [
    url(r'^djajax/update/$', views.djajax_endpoint, name='djajax-object-update-api'),
]
