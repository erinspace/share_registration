# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('push_endpoint', '0012_pusheddata_docid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pusheddata',
            old_name='collectionDateTime',
            new_name='firstCollectionDateTime',
        ),
        migrations.AddField(
            model_name='pusheddata',
            name='providerUpdatedDateTime',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 13, 15, 11, 22, 846917, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pusheddata',
            name='status',
            field=models.CharField(default='created', max_length=100),
            preserve_default=False,
        ),
    ]
