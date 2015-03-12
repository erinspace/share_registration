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
                ('oai_provider', models.CharField(max_length=1, choices=[(b'Y', b'yes'), (b'N', b'no')])),
                ('meta_tos', models.CharField(max_length=1, choices=[(b'Y', b'yes'), (b'N', b'no')])),
                ('meta_privacy', models.CharField(max_length=1, choices=[(b'Y', b'yes'), (b'N', b'no')])),
                ('meta_sharing_tos', models.CharField(max_length=1, choices=[(b'Y', b'yes'), (b'N', b'no')])),
                ('meta_license', models.CharField(max_length=100)),
                ('meta_license_extended', models.CharField(max_length=1, choices=[(b'Y', b'yes'), (b'N', b'no')])),
                ('meta_future_license', models.CharField(max_length=1, choices=[(b'Y', b'yes'), (b'N', b'no')])),
                ('property_list', models.TextField()),
                ('approved_sets', models.TextField()),
                ('registration_date', models.DateTimeField(verbose_name=b'date registered')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
