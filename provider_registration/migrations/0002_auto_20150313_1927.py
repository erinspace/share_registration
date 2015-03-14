# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('provider_registration', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrationinfo',
            name='contact_email',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='registrationinfo',
            name='contact_name',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
