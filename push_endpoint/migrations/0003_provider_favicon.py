# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('push_endpoint', '0002_auto_20151030_1033'),
    ]

    operations = [
        migrations.AddField(
            model_name='provider',
            name='favicon',
            field=models.BinaryField(null=True),
        ),
    ]
