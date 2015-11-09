# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('push_endpoint', '0007_auto_20151105_1444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='provider',
            name='longname',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Name'),
        ),
    ]
