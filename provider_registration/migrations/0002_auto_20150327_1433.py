# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('provider_registration', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='registrationinfo',
            options={'verbose_name': 'Registration'},
        ),
        migrations.AddField(
            model_name='registrationinfo',
            name='active_provider',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
