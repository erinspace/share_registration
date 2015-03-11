# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('push_endpoint', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pusheddata',
            name='owner',
            field=models.ForeignKey(related_name='data', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
