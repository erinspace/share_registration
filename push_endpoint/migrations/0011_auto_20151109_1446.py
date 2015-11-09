# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('push_endpoint', '0010_remove_provider_favicon_bytes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='provider',
            name='favicon_dataurl',
            field=models.TextField(null=True, verbose_name=b'Favicon Data URL'),
        ),
        migrations.AlterField(
            model_name='provider',
            name='favicon_image',
            field=models.ImageField(null=True, upload_to=b'shareregistration/static/img/favicons', blank=True),
        ),
    ]
