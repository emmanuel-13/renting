#!/usr/bin/env python
# -*- coding: utf8 -*-
from __future__ import absolute_import, division, generators, nested_scopes, print_function, unicode_literals, with_statement

import json
import logging

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models.signals import post_save
from django.db.models.signals import post_delete
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from django_middleware_global_request.middleware import get_request

from fastutils import dictutils
from magic_import import import_from_string

from .utils import get_item_data

logger = logging.getLogger(__name__)


def default_get_user_information(user):
    return {
        "username": user.username,
        "name": user.last_name + user.first_name,
        "email": user.email,
    }

class DataHistoryBase(models.Model):
    CREATE = "create"
    CHANGE = "change"
    DELETE = "delete"
    ACTION_CHOICES = [
        (CREATE, _("Create")),
        (CHANGE, _("Change")),
        (DELETE, _("Delete")),
    ]

    app_label = models.CharField(max_length=128, verbose_name=_("App Label"))
    model_name = models.CharField(max_length=128, verbose_name=_("Model Name"))
    item_id = models.BigIntegerField(verbose_name=_("Item Id"))
    version = models.IntegerField(verbose_name=_("Version"))
    request_id = models.CharField(max_length=128, null=True, blank=True, verbose_name=_("Request Id"))
    add_time = models.DateTimeField(auto_now_add=True, verbose_name=_("Add Time"))
    username = models.CharField(max_length=64, null=True, blank=True, verbose_name=_("Username"))
    userinfo = models.TextField(null=True, blank=True, verbose_name=_("User Information"))
    action = models.CharField(max_length=16, choices=ACTION_CHOICES, verbose_name=_("Action"))
    data = models.TextField(verbose_name=_("Data"))

    class Meta:
        abstract = True
        verbose_name = _("Data History")
        verbose_name_plural = _("Data Histories")
        indexes = [
            models.Index(fields=["app_label", "model_name", "item_id", "version"]),
            models.Index(fields=["username"]),
        ]

    # settings.py: GET_USER_INFORMATION
    # default_get_user_information

    def __str__(self):
        return "{app_label}.{model_name}.{item_id}.{version}".format(
            app_label=self.app_label,
            model_name=self.model_name,
            item_id=self.item_id,
            version=self.version,
        )

    @classmethod
    def get_user_information(cls, user):
        if hasattr(cls, "default_get_user_information"):
            return getattr(cls, "default_get_user_information")(user)
        if hasattr(settings, "GET_USER_INFORMATION"):
            method_path = getattr(settings, "GET_USER_INFORMATION")
            method = import_from_string(method_path)
            if method:
                return method(user)
        return default_get_user_information(user)

    def get_history_info(self):
        try:
            return json.loads(self.data)
        except:
            return {}

    def get_userinfo(self):
        try:
            return json.loads(self.userinfo)
        except:
            return {
                "username": self.username,
            }

    def userinfo_display(self):
        return str(render_to_string("django_data_history/userinfo.html", self.get_userinfo()))

    def userinfo_text(self):
        lines = []
        for field, value in self.get_userinfo().items():
            line = "{field}: {value}".format(
                field=field,
                value=value,
            )
            lines.append(line)
        return "\n".join(lines)

    def changes_count(self):
        return len(self.get_history_info().get("changes", {})) or 1

    def get_all_changes(self):
        changes = []
        for field, values in self.get_history_info().get("changes", {}).items():
            changes.append({
                "field": field,
                "old_value": values[0] or "-",
                "new_value": values[1] or "-",
            })
        return changes

    def get_first_changes(self):
        changes = self.get_all_changes()
        if changes:
            return changes[0]
        else:
            return {
                "field": "-",
                "old_value": "-",
                "new_value": "-",
            }

    def get_more_changes(self):
        return self.get_all_changes()[1:]

    @classmethod
    def get_data_histories(cls, app_label, model_name, item_id):
        return cls.objects.filter(app_label=app_label, model_name=model_name, item_id=item_id).order_by("-version").all()

    @classmethod
    def get_data_history(cls, app_label, model_name, item_id):
        latest_history_item = cls.objects.filter(app_label=app_label, model_name=model_name, item_id=item_id).order_by("-version").first()
        return latest_history_item

    @classmethod
    def add_data_history(cls, item, action, username=None, userinfo=None, save=True, ignore_unchanged_version=True):
        nowtime = timezone.now()
        request = get_request()
        request_id = getattr(request, "request_id", None)

        app_label = item._meta.app_label
        model_name = item._meta.model_name
        latest_history_item = cls.get_data_history(app_label, model_name, item.pk)

        if latest_history_item:
            new_version = latest_history_item.version + 1
            info = latest_history_item.get_history_info()
            old_data = info.get("data")
            old_delete_flag = info.get("delete_flag", False)
        else:
            new_version = 1
            old_data = {}
            old_delete_flag = False

        new_data = get_item_data(item)
        _, changed_keys = dictutils.changes(old_data, new_data, keys=list(new_data.keys()), return_changed_keys=True, do_update=False)
        if action == cls.DELETE: # 当前是删除记录
            if old_delete_flag: # 如果上一次是删除记录，则忽略本次记录
                return None
            else: # 否则需要记录
                pass
        else:
            if not changed_keys: # 如果没有数据变更
                if ignore_unchanged_version: # 如果要求忽略无数据变更的保存，则忽略本次记录
                    return None
                else: # 否则保存本次记录
                    pass
            else: # 有数据变更，则保存本次记录
                pass

        changes = {}
        for key in changed_keys:
            old_value = old_data.get(key, None)
            new_value = new_data.get(key, None)
            changes[key] = (old_value, new_value)

        if request and request.user and request.user.pk:
            username = request.user.username
            userinfo = cls.get_user_information(request.user)

        new_history = cls()
        new_history.app_label = app_label
        new_history.model_name = model_name
        new_history.item_id = item.pk
        new_history.version = new_version
        new_history.add_time = nowtime
        new_history.username = username
        new_history.userinfo = json.dumps(userinfo)
        new_history.request_id = request_id
        new_history.action = action
        new_history.data = json.dumps({
            "app_label": app_label,
            "model_name": model_name,
            "item_id": item.pk,
            "add_item": timezone.make_naive(nowtime).strftime("%Y-%m-%d %H:%M:%S"),
            "data": new_data,
            "changes": changes,
            "username": username,
            "userinfo": userinfo,
            "request_id": request_id,
            "action": action,
            "version": new_version,
        }, indent=4)
        if save:
            new_history.save()
        return new_history

SAVE_DATA_HISTORIES_FLAG = "save_data_histories_flag"

class DataHistory(DataHistoryBase):

    class Meta:
        verbose_name = _("Data History")
        verbose_name_plural = _("Data Histories")

def get_data_history_storage_class(instance_or_model_class):
    return getattr(instance_or_model_class, "DATA_HISTORY_STORAGE_CLASS", DataHistory)

def save_data_histories_for_fk_instance(instance):
    for field in instance._meta.fields:
        if isinstance(field, models.ForeignKey):
            fk_instance = getattr(instance, field.name)
            DataHistoryModel = get_data_history_storage_class(fk_instance)
            DataHistoryModel.add_data_history(fk_instance, action=DataHistoryModel.CHANGE, ignore_unchanged_version=True, save=True)

def save_data_histories_for(Model):
    DataHistoryModel = get_data_history_storage_class(Model)

    app_label = Model._meta.app_label
    model_name = Model._meta.model_name
    post_save_func_name = "save_data_histories_for_{app_label}_{model_name}_on_post_save".format(
        app_label=app_label,
        model_name=model_name,
    )
    post_delete_func_name = "save_data_histories_for_{app_label}_{model_name}_on_post_delete".format(
        app_label=app_label,
        model_name=model_name,
    )
    msg = "adding save_data_histories_flag for model: {app_label}.{model_name}".format(
        app_label=app_label,
        model_name=model_name,
    )
    logger.debug(msg)
    setattr(Model, SAVE_DATA_HISTORIES_FLAG, True)

    if not hasattr(Model, post_save_func_name):
        msg = "registering signal handler: {post_save_func_name}...".format(
            post_save_func_name=post_save_func_name,
        )
        logger.debug(msg)
        @receiver(post_save, sender=Model)
        def model_post_save(sender, instance, **kwargs):
            created = kwargs.get("created", False)
            if created:
                DataHistoryModel.add_data_history(instance, action=DataHistoryModel.CREATE, ignore_unchanged_version=True, save=True)
            else:
                DataHistoryModel.add_data_history(instance, action=DataHistoryModel.CHANGE, ignore_unchanged_version=True, save=True)
            save_data_histories_for_fk_instance(instance)
        setattr(Model, post_save_func_name, model_post_save)

    if not hasattr(Model, post_delete_func_name):
        msg = "registering signal handler: {post_delete_func_name}...".format(
            post_delete_func_name=post_delete_func_name,
        )
        logger.debug(msg)
        @receiver(post_delete, sender=Model)
        def model_post_delete(sender, instance, **kwargs):
            DataHistoryModel.add_data_history(instance, action=DataHistoryModel.DELETE, ignore_unchanged_version=True, save=True)
            save_data_histories_for_fk_instance(instance)
        setattr(Model, post_delete_func_name, model_post_delete)
    
    for field in Model._meta.many_to_many:
        field_name = field.name
        m2m_changed_func_name = "save_data_histories_for_{app_label}_{model_name}_{field_name}_on_m2m_changed".format(
            app_label=app_label,
            model_name=model_name,
            field_name=field_name,
        )

        if not hasattr(Model, m2m_changed_func_name):
            msg = "registering signal handler: {m2m_changed_func_name}...".format(
                m2m_changed_func_name=m2m_changed_func_name,
            )
            logger.debug(msg)
            @receiver(m2m_changed, sender=getattr(getattr(Model, field.name), "through"))
            def model_m2m_changed(sender, instance, **kwargs):
                DataHistoryModel.add_data_history(instance, action=DataHistoryModel.CHANGE, ignore_unchanged_version=True, save=True)
                save_data_histories_for_fk_instance(instance)
            setattr(Model, m2m_changed_func_name, model_m2m_changed)


def add_save_data_histories_flag_for_all_models():
    msg = "adding save_data_histories_flag for all models..."
    logger.debug(msg)

    from django.apps import apps
    SYSTEM_MODELS_DO_NOT_SAVE_DATA_HISTORIES = getattr(settings, "SYSTEM_MODELS_DO_NOT_SAVE_DATA_HISTORIES", [
        "sessions.session",
        "contenttypes.contenttype",
        "admin.logentry",
        "auth.permission",
    ])
    SAVE_DATA_HISTORIES_FOR_ALL = getattr(settings, "SAVE_DATA_HISTORIES_FOR_ALL", False)
    SAVE_DATA_HISTORIES_FOR = getattr(settings, "SAVE_DATA_HISTORIES_FOR", [])
    DO_NOT_SAVE_DATA_HISTORIES_FOR = set(getattr(settings, "DO_NOT_SAVE_DATA_HISTORIES_FOR", []) + SYSTEM_MODELS_DO_NOT_SAVE_DATA_HISTORIES)

    if SAVE_DATA_HISTORIES_FOR_ALL:
        for Model in apps.get_models():
            if issubclass(Model, DataHistoryBase):
                continue
            app_label = Model._meta.app_label
            model_name = Model._meta.model_name
            info = app_label + "." + model_name
            if not info in DO_NOT_SAVE_DATA_HISTORIES_FOR:
                save_data_histories_for(Model)
    else:
        for info in SAVE_DATA_HISTORIES_FOR:
            app_label, model_name = info.split(".")
            Model = apps.get_model(app_label=app_label, model_name=model_name)
            if issubclass(Model, DataHistoryBase):
                continue
            save_data_histories_for(Model)

def get_histories(instance):
    DataHistoryModel = get_data_history_storage_class(instance)
    return DataHistoryModel.objects.filter(
        app_label=instance._meta.app_label,
        model_name=instance._meta.model_name,
        item_id=instance.pk,
    ).order_by("-version")

def get_deleted_instance_histories(ModelClass, pk):
    DataHistoryModel = get_data_history_storage_class(ModelClass)
    return DataHistoryModel.objects.filter(
        app_label=ModelClass._meta.app_label,
        model_name=ModelClass._meta.model_name,
        item_id=pk,
    ).order_by("-version")
