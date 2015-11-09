# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('push_endpoint', '0009_provider_favicon_dataurl'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='provider',
            name='favicon_bytes',
        ),
    ]
