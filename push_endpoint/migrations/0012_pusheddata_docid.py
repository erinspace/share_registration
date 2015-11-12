# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('push_endpoint', '0011_auto_20151109_1446'),
    ]

    operations = [
        migrations.AddField(
            model_name='pusheddata',
            name='docID',
            field=models.TextField(default='http://url.com'),
            preserve_default=False,
        ),
    ]
