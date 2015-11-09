# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('push_endpoint', '0008_auto_20151106_1643'),
    ]

    operations = [
        migrations.AddField(
            model_name='provider',
            name='favicon_dataurl',
            field=models.TextField(max_length=255, null=True, verbose_name=b'Favicon Data URL'),
        ),
    ]
