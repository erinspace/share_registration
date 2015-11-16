# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('push_endpoint', '0018_pusheddata_datasource'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pusheddata',
            old_name='source',
            new_name='user',
        ),
    ]
