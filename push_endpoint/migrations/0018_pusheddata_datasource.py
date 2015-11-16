# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('push_endpoint', '0017_auto_20151113_1532'),
    ]

    operations = [
        migrations.AddField(
            model_name='pusheddata',
            name='datasource',
            field=models.CharField(default='test', max_length=100),
            preserve_default=False,
        ),
    ]
