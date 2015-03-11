# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('push_endpoint', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pusheddata',
            old_name='data',
            new_name='contributors',
        ),
        migrations.AddField(
            model_name='pusheddata',
            name='dateUpdated',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pusheddata',
            name='description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pusheddata',
            name='doi',
            field=models.TextField(default=11),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pusheddata',
            name='serviceID',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pusheddata',
            name='source',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pusheddata',
            name='tags',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pusheddata',
            name='title',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pusheddata',
            name='url',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
