# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('push_endpoint', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pusheddata',
            name='description',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pusheddata',
            name='tags',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
    ]
