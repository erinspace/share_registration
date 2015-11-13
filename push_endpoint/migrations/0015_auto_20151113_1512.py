# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('push_endpoint', '0014_auto_20151113_1335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pusheddata',
            name='status',
            field=models.CharField(default=b'created', max_length=100),
        ),
    ]
