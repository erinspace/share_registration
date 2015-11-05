# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('push_endpoint', '0003_provider_favicon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='provider',
            name='favicon',
            field=models.ImageField(null=True, upload_to=b'favicons'),
        ),
    ]
