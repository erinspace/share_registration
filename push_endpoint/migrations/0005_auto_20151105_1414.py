# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('push_endpoint', '0004_auto_20151105_0932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='provider',
            name='favicon',
            field=models.ImageField(null=True, upload_to=b'static/img/favicons'),
        ),
    ]
