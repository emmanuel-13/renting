#!/usr/bin/env python
# -*- coding: utf8 -*-
from __future__ import absolute_import, division, generators, nested_scopes, print_function, unicode_literals, with_statement

default_app_config = "django_data_history.apps.DjangoDataHistoryConfig"

app_requires = [
    "django_middleware_global_request",
    "django_static_jquery_ui",
]

app_middleware_requires = [
    "django_middleware_global_request.middleware.GlobalRequestMiddleware",
    "django_data_history.middlewares.HttpXRequestIdMiddleware",
]
