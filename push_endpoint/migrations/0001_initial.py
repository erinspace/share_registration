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
            name='Provider',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('established', models.BooleanField(default=False)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PushedData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField()),
                ('doi', models.TextField()),
                ('title', models.TextField()),
                ('serviceID', models.TextField()),
                ('contributors', models.TextField()),
                ('tags', models.TextField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('dateUpdated', models.DateField(auto_now_add=True)),
                ('source', models.ForeignKey(related_name='data', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Data Object',
            },
            bases=(models.Model,),
        ),
    ]
