# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('push_endpoint', '0021_auto_20151116_1318'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pusheddata',
            old_name='user',
            new_name='provider',
        ),
    ]
