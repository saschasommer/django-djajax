# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse

from django.conf import settings


__all__ = ('JSONResponse', 'CSVResponse')


# Taken from bakery: https://github.com/muffins-on-dope/bakery
# License: BSD
# https://github.com/muffins-on-dope/bakery/blob/9bd3b6b93b/bakery/api/views.py
DUMPS_KWARGS = {
    'cls': DjangoJSONEncoder,
    'indent': True if settings.DEBUG else None
}


class JSONResponse(HttpResponse):

    def __init__(self, data, status=200, content_type='application/json',
            **kwargs):
        """
        Create a new HTTP response which content_type defaults to
        ``'application/json'``.

        :param data: Any data type the
            :class:`~django.core.serializers.json.DjangoJSONEncoder` can
            handle (unless a different class is defined).
        :param int status: The HTTP response code. (Defaults to 200)
        :param str content_type: The content type for the response. (Defaults
            to ``'application/json'``)
        :param kwargs: Any additional kwargs are passed to the ``json.dumps``
            call.
        """
        ekwargs = {}
        ekwargs.update(DUMPS_KWARGS)
        dump = json.dumps(data, **ekwargs)
        super(JSONResponse, self).__init__(
            content=dump, status=status, content_type=content_type
        )


