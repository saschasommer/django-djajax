=============
django-djajax
=============



Purpose
=======

A Django library that integrates Ajax model change functionality into templates, 
so one can attach form inputs to backend models. 


WARNING!
========

Djajax is an experimental django app, currently deep in its first iteration. 
The app still has major security flaws because of its experimental nature.


I recommend you DON'T USE djajax in your project yet, 
especially if it is running in a production environment!


Install
=======

To integrate ``django-djajax`` with your site, there are few things
that are required:

#. Installing::

       pip install -e git://github.com/saschan/django-djajax.git@master#egg=django-djajax

#. List this application in the ``INSTALLED_APPS`` portion of your settings file.
   Your settings file will look something like::

        INSTALLED_APPS = (
            ...
            'djajax',
        )

#. Add the djajax URL config to your root URL config: ::

        urlpatterns += patterns('',
            ...,
            url(r'^', include('djajax.urls', namespace='djajax')),
        )
        
        
Usage examples
==============

This documentation is very incomplete as of now. More details and examples will be added later on. 

Here is a very simple quick example:

What we will do is connect an input box in a model form with the model attribute. Whenever a specified
Javascript event is triggered on the client (default: enter key pressed), the connected model attribute
is updated in the backend via an AJAX call. The necessary javascript functions are generated automatically
by djajax.

What you have to do:

#. Prepare your template:
    * Add ``{% load djajax_tags %}`` to the top of your template
    * Add ``{% djajax generate %}`` to the footer of your template.

#. In your django template:
    Connect the model attribute. Here, we have a todo entry and want to be able to change the todo's title
    attribute via an AJAX call whenever the input's value is changed or the field loses focus: ::
    
       <input value="{{ todo.title }}" {% djajax_connect todo.title trigger_on="enter_key,lose_focus" empty="false" %} />
              
    This doesn't necessarily need to be located in a <form> tag. A csrf cookie will be automatically generated
    for the AJAX call.
    
    Available triggers are: ``enter_key``, ``lose_focus``, ``click``, ``value_changed`` (this one can be spammy!).
    
    Since ``empty="false"`` is set, if the user attempts to submit an empty value, the input is reset
    to its last known value, and no model change happens.
    
Global Settings
===============

Django's ``settings.py``::
    
    # Lets you specify a different Djajax endpoint, which can override the existing one. 
    # Especially useful to specify custom write permissions for backend models.
    DJAJAX_VIEW_CLASS = 'djajax.views.DjajaxEndpoint'
    

Custom Djajax Endpoints
=======================

Example for a custom endpoint: ::

       from djajax.views import DjajaxEndpoint
       class DjajaxCosinnusEndpoint(DjajaxEndpoint):
              def check_write_permissions(self, obj, user):
                     """ Better permission checks """
                     return user.is_authenticated() and obj.creator == user

.. _django-djajax: https://github.com/saschan/django-djajax
