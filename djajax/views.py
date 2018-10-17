# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import apps
from django.views.generic.base import View
from importlib import import_module
from django.conf import settings

from djajax.utils.http import JSONResponse
from djajax.defaults import DJAJAX_ALLOWED_ACCESSES



DEFAULT_DJAJAX_VIEW_CLASS = 'djajax.views.DjajaxEndpoint'

    
def _resolve_class(path_to_class):
    modulename, _, klass = path_to_class.rpartition('.')
    module = import_module(modulename)
    cls = getattr(module, klass, None)
    if cls is None:
        raise ImportError("Cannot import class %s from %s" % (
            klass, path_to_class))
    return cls


class DjajaxEndpoint(View):
    
    def check_write_permissions(self, obj, user, **kwargs):
        """ Permissions check if ``user`` may modify ``obj``.
            Defaults to checking if the user is logged in.
            It is highly recommended to override this method to add your own security checks!
        """
        return user.is_authenticated()
    
    def dispatch(self, request, *args, **kwargs):
        """
            An introspective API endpoint that allows modification of arbitraty django models.
            
            The request must be a POST, be authenticated and supply a csrf token.
            
            By a given app_label, model_name and pk, the model instance to be modified is resolved.
                - write permissions will be checked for that instance via an extensible permission function.
            
            By a given property_name, the field that is supposed to be updated is resolved
                - the field value will be set to ``property_data`` and the instance will be saved
                - Only django fields that are set to be editable can be changed.
                - Related fields are supported. 
                    - We expect ``property_data`` to be the pk of the 
                    related field's target.
                    - The target of the related pk will attempted to be found via the model class set in the
                    related field. If it is not found, the related field's value will be set to None.
                    
        """
        if request.method == "POST":
            # TODO: Django<=1.5: Django 1.6 removed the cookie check in favor of CSRF
            #request.session.set_test_cookie()
            
            app_label = request.POST.get('app_label')
            model_name = request.POST.get('model_name')
            pk = request.POST.get('pk')
            property_name = request.POST.get('property_name')
            property_data = request.POST.get('property_data')
            
            # pre-check in settings: is model and attributes in access white-list?
            attribute_list = DJAJAX_ALLOWED_ACCESSES.get('%s.%s' % (app_label, model_name), None)
            if not attribute_list or not property_name in attribute_list:
                return JSONResponse(data={'status':'error', 'reason':'This object cannot be modified! (%s_%s.%s)' \
                                          % (app_label, model_name, property_name)}, status=403)
            
            # resolve model class and get instance
            model_class = apps.get_model(app_label, model_name)
            if not model_class:
                return JSONResponse('Model class %s.%s not found!' % (app_label, model_name), status=400)
            try:
                instance = model_class._default_manager.get(pk=pk)
            except model_class.DoesNotExist:
                instance = None
            if not instance:
                return JSONResponse('Object with pk "%s" not found for class "%s"!' % (pk, model_class), status=400)
            
            #check permissions:
            if not self.check_write_permissions(instance, request.user, fields=[property_name]):
                return JSONResponse('You do not have the necessary permissions to modify this object!', status=403)
            
            # check field exists
            fields = model_class._meta.get_field_by_name(property_name)
            field = fields[0] if fields else None
            if not field or not field.editable:
                return JSONResponse('Field "%s" not found for class "%s"!' % (property_name, model_class), status=400)
    
            # resolve supplied ids for related fields
            is_related_field = hasattr(field, 'related')
            if is_related_field:
                related_class = getattr(field.related, 'parent_model', getattr(field.related, 'model')) # pre django 1.8 compat
                try:
                    property_data = related_class._default_manager.get(pk=property_data)
                except related_class.DoesNotExist:
                    property_data = None
            
            value = getattr(instance, property_name, None)
            
            dict_key = None
            if type(value) is dict:
                # we have a dictionary, set its key to the split data
                try:
                    dict_key, property_data = property_data.split(':', 1)
                except ValueError:
                    raise Exception("Could not split value %s into a 'key,value' pair. Is the value seperated with a colon?" % property_data)
                value[dict_key] = property_data
            else:
                # attempt the change the object's attribute
                setattr(instance, property_name, property_data)
            instance.save()
            
            # for related fields, return the pk instead of the object
            return_value =  getattr(instance, property_name, '')
            if dict_key:
                return_value = return_value[dict_key]
            # if the save was not successful we return the data as it is in the backend
            if return_value != property_data:
                return JSONResponse({'status':'error', 'property_name': property_name, 'property_data': return_value})
    
            if return_value and is_related_field:
                return_value = return_value.pk
            
            return JSONResponse({'status':'success', 'property_name': property_name, 'property_data': return_value})
        else:
            return JSONResponse({}, status=405)  # Method not allowed



djajax_endpoint = _resolve_class(getattr(settings, 'DJAJAX_VIEW_CLASS', DEFAULT_DJAJAX_VIEW_CLASS)).as_view()
