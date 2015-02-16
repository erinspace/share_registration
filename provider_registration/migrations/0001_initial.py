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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('provider_name', models.CharField(max_length=100)),
                ('base_url', models.CharField(max_length=100)),
                ('property_list', models.TextField()),
                ('approved_sets', models.TextField()),
                ('registration_date', models.DateTimeField(verbose_name=b'date registered')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
