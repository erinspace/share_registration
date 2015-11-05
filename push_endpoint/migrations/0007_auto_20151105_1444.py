# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('push_endpoint', '0006_auto_20151105_1414'),
    ]

    operations = [
        migrations.RenameField(
            model_name='provider',
            old_name='favicon',
            new_name='favicon_image',
        ),
        migrations.AddField(
            model_name='provider',
            name='favicon_bytes',
            field=models.BinaryField(null=True),
        ),
    ]
