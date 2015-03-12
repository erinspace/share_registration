# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('provider_registration', '0005_auto_20150309_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrationinfo',
            name='base_url',
            field=models.URLField(),
            preserve_default=True,
        ),
    ]
