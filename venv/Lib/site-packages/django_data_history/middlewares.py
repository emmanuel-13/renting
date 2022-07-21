#!/usr/bin/env python
# -*- coding: utf8 -*-
from __future__ import absolute_import, division, generators, nested_scopes, print_function, unicode_literals, with_statement

import uuid
from django.conf import settings

class HttpXRequestIdMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response
        self.header_name = getattr(settings, "REQUEST_ID_HEADER", "HTTP_X_REQUEST_ID")
        self.auto_generate_request_id = getattr(settings, "AUTO_GENERATE_REQUEST_ID", True)

    def __call__(self, request, *args, **kwargs):
        http_x_request_id = request.META.get(self.header_name, None)
        if (http_x_request_id is None) and self.auto_generate_request_id:
            http_x_request_id = uuid.uuid4().hex
        setattr(request, "request_id", http_x_request_id)
        return self.get_response(request, *args, **kwargs)
