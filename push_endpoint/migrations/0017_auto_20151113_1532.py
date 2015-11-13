# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('push_endpoint', '0016_remove_pusheddata_updated'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pusheddata',
            name='created',
        ),
        migrations.AddField(
            model_name='pusheddata',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 13, 20, 32, 35, 608984, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
