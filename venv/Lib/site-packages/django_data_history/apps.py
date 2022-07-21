#!/usr/bin/env python
# -*- coding: utf8 -*-
from __future__ import absolute_import, division, generators, nested_scopes, print_function, unicode_literals, with_statement

import logging
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)

class DjangoDataHistoryConfig(AppConfig):
    name = "django_data_history"
    verbose_name = _("Django Data History")

    def ready(self):
        from .models import add_save_data_histories_flag_for_all_models
        from .admin import fix_data_histories_model_admin_for_all_models_with_save_data_histories_flag

        add_save_data_histories_flag_for_all_models()
        fix_data_histories_model_admin_for_all_models_with_save_data_histories_flag()