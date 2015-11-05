# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('push_endpoint', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='provider',
            name='longname',
            field=models.CharField(max_length=255, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='provider',
            name='shortname',
            field=models.CharField(max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='provider',
            name='url',
            field=models.URLField(max_length=255, null=True),
            preserve_default=True,
        ),
    ]
