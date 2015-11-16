# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('push_endpoint', '0019_auto_20151116_1244'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pusheddata',
            old_name='datasource',
            new_name='source',
        ),
    ]
