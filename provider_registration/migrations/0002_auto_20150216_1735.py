# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('provider_registration', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registrationinfo',
            name='id',
        ),
        migrations.AlterField(
            model_name='registrationinfo',
            name='provider_name',
            field=models.CharField(max_length=100, serialize=False, primary_key=True),
            preserve_default=True,
        ),
    ]
