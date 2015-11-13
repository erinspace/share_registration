# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('push_endpoint', '0013_auto_20151113_1011'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pusheddata',
            old_name='firstCollectionDateTime',
            new_name='created',
        ),
        migrations.RenameField(
            model_name='pusheddata',
            old_name='providerUpdatedDateTime',
            new_name='updated',
        ),
    ]
