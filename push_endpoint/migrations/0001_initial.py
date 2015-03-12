# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PushedData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField()),
                ('contributors', models.TextField()),
                ('tags', models.TextField()),
                ('title', models.TextField()),
                ('dateUpdated', models.DateField()),
                ('url', models.URLField()),
                ('serviceID', models.TextField()),
                ('doi', models.TextField()),
                ('source', models.ForeignKey(related_name='data', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
