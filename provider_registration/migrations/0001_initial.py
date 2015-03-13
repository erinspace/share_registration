# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RegistrationInfo',
            fields=[
                ('provider_short_name', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('provider_long_name', models.CharField(max_length=100)),
                ('base_url', models.URLField()),
                ('description', models.TextField()),
                ('oai_provider', models.BooleanField(default=False)),
                ('meta_tos', models.BooleanField(default=False)),
                ('meta_privacy', models.BooleanField(default=False)),
                ('meta_sharing_tos', models.BooleanField(default=False)),
                ('meta_license', models.CharField(max_length=100)),
                ('meta_license_extended', models.BooleanField(default=False)),
                ('meta_future_license', models.BooleanField(default=False)),
                ('property_list', models.TextField()),
                ('approved_sets', models.TextField()),
                ('registration_date', models.DateTimeField(verbose_name=b'date registered')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
