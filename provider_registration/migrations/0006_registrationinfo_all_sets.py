# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('provider_registration', '0005_auto_20151106_1637'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrationinfo',
            name='all_sets',
            field=models.BooleanField(default=False),
        ),
    ]
