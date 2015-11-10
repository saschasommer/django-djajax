# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings

# The white-list of model classes and attributes that may be accessed and changed by djajax.
# This is a white-list only, with no wildcards on purpose, so that no accidental vulnerabilites
# are introduced.
# Example:
# DJAJAX_ALLOWED_ACCESSES = {
#    'myapp.MyModel': ('property1', 'property2', )
# }


DJAJAX_ALLOWED_ACCESSES = getattr(settings, 'DJAJAX_ALLOWED_ACCESSES', {})



