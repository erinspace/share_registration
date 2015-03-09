# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('provider_registration', '0002_auto_20150216_1735'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrationinfo',
            name='description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
