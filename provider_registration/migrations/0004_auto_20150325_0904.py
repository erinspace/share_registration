# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('provider_registration', '0003_auto_20150325_0903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrationinfo',
            name='request_rate_limit',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=True,
        ),
    ]
