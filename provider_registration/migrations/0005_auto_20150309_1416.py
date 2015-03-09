# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('provider_registration', '0004_auto_20150309_1244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrationinfo',
            name='meta_license',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
    ]
