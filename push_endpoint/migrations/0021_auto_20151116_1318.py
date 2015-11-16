# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('push_endpoint', '0020_auto_20151116_1244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pusheddata',
            name='user',
            field=models.ForeignKey(related_name='data', to='push_endpoint.Provider'),
        ),
    ]
