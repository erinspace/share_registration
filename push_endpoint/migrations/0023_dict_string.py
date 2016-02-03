# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import ast
import six
import json
from django.db import migrations, models


def forwards_func(apps, schema_editor):
    # Takes strings, lieral evals them into python Dicts
    PushedData = apps.get_model("push_endpoint", "PushedData")
    for item in PushedData.objects.all():
        if isinstance(item.jsonData, six.string_types):
            item.jsonData = ast.literal_eval(json.loads(json.dumps(item.jsonData)))
            item.save()


def reverse_func(apps, schema_editor):
    # Puts dicts back into literal strings
    PushedData = apps.get_model("push_endpoint", "PushedData")
    for item in PushedData.objects.all():
        if isinstance(item.jsonData, dict):
            item.jsonData = six.u(item)
            item.save()


class Migration(migrations.Migration):

    dependencies = [
        ('push_endpoint', '0022_auto_20151116_1341'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
