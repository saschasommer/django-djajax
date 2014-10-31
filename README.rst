=============
django-djajax
=============



Purpose
=======



Install
=======

To integrate ``django-djajax`` with your site, there are few things
that are required:

#. Installing::

       pip install django-djajx

#. List this application in the ``INSTALLED_APPS`` portion of your settings file.
   Your settings file will look something like::

        INSTALLED_APPS = (
            ...
            'djajax',
        )

#. Add the djajax URL config to your root URL config:


        urlpatterns += patterns('',
            ...
            url(r'^', include('djajax.urls', namespace='djajax')),
        )
        
        
Usage examples
==============

        
Global Settings
===============

Django's ``settings.py``::
    
     
.. _django-djajax: https://github.com/j
