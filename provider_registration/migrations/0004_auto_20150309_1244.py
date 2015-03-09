# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('provider_registration', '0003_registrationinfo_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrationinfo',
            name='meta_future_license',
            field=models.CharField(default='Y', max_length=1, choices=[(b'Y', b'yes'), (b'N', b'no')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='registrationinfo',
            name='meta_license',
            field=models.CharField(default='Y', max_length=1, choices=[(b'Y', b'yes'), (b'N', b'no')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='registrationinfo',
            name='meta_license_extended',
            field=models.CharField(default='Y', max_length=1, choices=[(b'Y', b'yes'), (b'N', b'no')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='registrationinfo',
            name='meta_privacy',
            field=models.CharField(default='Y', max_length=1, choices=[(b'Y', b'yes'), (b'N', b'no')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='registrationinfo',
            name='meta_sharing_tos',
            field=models.CharField(default='Y', max_length=1, choices=[(b'Y', b'yes'), (b'N', b'no')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='registrationinfo',
            name='meta_tos',
            field=models.CharField(default='Y', max_length=1, choices=[(b'Y', b'yes'), (b'N', b'no')]),
            preserve_default=False,
        ),
    ]
