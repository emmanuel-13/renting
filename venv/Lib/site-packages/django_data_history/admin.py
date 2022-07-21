#!/usr/bin/env python
# -*- coding: utf8 -*-
from __future__ import absolute_import, division, generators, nested_scopes, print_function, unicode_literals, with_statement

import logging

from django.contrib import admin

from .models import DataHistory
from .models import SAVE_DATA_HISTORIES_FLAG
from .utils import post_admin_autodiscover


logger = logging.getLogger(__name__)


class DataHistoryAdmin(admin.ModelAdmin):
    list_display = ["pk", "app_label", "model_name", "item_id", "version", "action", "add_time"]
    list_filter = ["app_label", "model_name", "action", "add_time"]
    search_fields = ["item_id"]


class DataHistoryModelAdmin(admin.ModelAdmin):
    
    def history_view(self, request, object_id, extra_context=None):
        extra_context = extra_context or {}
        extra_context["using_django_data_history_view"] = True
        extra_context["django_data_histories"] = self.get_data_histories(object_id)
        extra_context["media"] = self.media
        return super().history_view(request, object_id, extra_context)

    def get_data_histories(self, item_id):
        item_id = int(item_id)
        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name
        DataHistoryModel = getattr(self.model, "DATA_HISTORY_MODEL", DataHistory)
        data_histories = DataHistoryModel.get_data_histories(app_label, model_name, item_id)
        return data_histories

    class Media:
        css = {
            "all": [
                "jquery-ui/jquery-ui.min.css",
                "django_data_history/css/django_data_history.css",
            ]
        }
        js = [
            "admin/js/vendor/jquery/jquery.js",
            "jquery-ui/jquery-ui.min.js",
            "django_data_history/js/django_data_history.js",
            "admin/js/jquery.init.js",
        ]

admin.site.register(DataHistory, DataHistoryAdmin)


def fix_data_histories_model_admin(Model, site=None):
    app_label = Model._meta.app_label
    model_name = Model._meta.model_name
    site = site or admin.site
    ModelAdminInstance = admin.site._registry.get(Model, None)

    if not ModelAdminInstance:
        return
    ModelAdminClass = ModelAdminInstance.__class__
    if issubclass(ModelAdminClass, DataHistoryModelAdmin):
        return

    msg = "fixing data histories model admin for: {app_label}.{model_name}".format(
        app_label=app_label,
        model_name=model_name,
    )
    logger.info(msg)
    class NewModelAdminWithDataHistories(DataHistoryModelAdmin, ModelAdminClass):
        pass
    site.unregister(Model)
    site.register(Model, NewModelAdminWithDataHistories)

def fix_data_histories_model_admin_for_all_models_with_save_data_histories_flag():
    def _fix_data_histories_model_admin_for_all_models_with_save_data_histories_flag():
        msg = "fixing data histories model admin for all models with save_data_histories_flag..."
        logger.info(msg)
        from django.apps import apps
        for Model in apps.get_models():
            if getattr(Model, SAVE_DATA_HISTORIES_FLAG, False):
                fix_data_histories_model_admin(Model)
    post_admin_autodiscover(_fix_data_histories_model_admin_for_all_models_with_save_data_histories_flag)
