# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('push_endpoint', '0015_auto_20151113_1512'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pusheddata',
            name='updated',
        ),
    ]
