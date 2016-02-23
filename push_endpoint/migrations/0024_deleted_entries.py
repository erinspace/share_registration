# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


LIST_OF_DOCIDS = [
    "https://scholarsphere.psu.edu/files/5712mj127",
    "https://scholarsphere.psu.edu/files/5712mj14s",
    "https://scholarsphere.psu.edu/files/5712mj152",
    "https://scholarsphere.psu.edu/files/5712mj16b",
    "https://scholarsphere.psu.edu/files/5712mj17m",
    "https://scholarsphere.psu.edu/files/5712mj18w",
    "https://scholarsphere.psu.edu/files/5712mj195",
    "https://scholarsphere.psu.edu/files/5712mj20x",
    "https://scholarsphere.psu.edu/files/5712mj216",
    "https://scholarsphere.psu.edu/files/5712mj22g",
    "https://scholarsphere.psu.edu/files/5712mj241",
    "https://scholarsphere.psu.edu/files/x346dn061",
    "https://scholarsphere.psu.edu/files/x346dn079",
    "https://scholarsphere.psu.edu/files/x346dn08k",
    "https://scholarsphere.psu.edu/files/x346dn09v",
    "https://scholarsphere.psu.edu/files/x346dn10m",
    "https://scholarsphere.psu.edu/files/x346dn13f",
    "https://scholarsphere.psu.edu/files/x346dn14q",
    "https://scholarsphere.psu.edu/files/x346dn168",
    "https://scholarsphere.psu.edu/files/x346dn18t",
    "https://scholarsphere.psu.edu/files/x346dn20v",
    "https://scholarsphere.psu.edu/files/x346dn214",
    "https://scholarsphere.psu.edu/files/x346dn24z",
    "https://scholarsphere.psu.edu/files/x346dn257",
    "https://scholarsphere.psu.edu/files/x346dn26h",
    "https://scholarsphere.psu.edu/files/x346dn27s",
    "https://scholarsphere.psu.edu/files/x346dn282",
    "https://scholarsphere.psu.edu/files/x346dn29b",
    "https://scholarsphere.psu.edu/files/x346dn303",
    "https://scholarsphere.psu.edu/files/x346dn32n",
    "https://scholarsphere.psu.edu/files/x346dn35g",
    "https://scholarsphere.psu.edu/files/x346dn371",
    "https://scholarsphere.psu.edu/files/x346dn389",
    "https://scholarsphere.psu.edu/files/x346dn39k",
    "https://scholarsphere.psu.edu/files/x346dn40b",
    "https://scholarsphere.psu.edu/files/x346dn41m",
    "https://scholarsphere.psu.edu/files/x346dn42w",
    "https://scholarsphere.psu.edu/files/x346dn435",
    "https://scholarsphere.psu.edu/files/x346dn460",
    "https://scholarsphere.psu.edu/files/x346dn478",
    "https://scholarsphere.psu.edu/files/x346dn48j",
    "https://scholarsphere.psu.edu/files/x346dn49t",
    "https://scholarsphere.psu.edu/files/x346dn50k",
    "https://scholarsphere.psu.edu/files/x346dn51v",
    "https://scholarsphere.psu.edu/files/x346dn53d",
    "https://scholarsphere.psu.edu/files/x346dn54p",
    "https://scholarsphere.psu.edu/files/x346dn567",
    "https://scholarsphere.psu.edu/files/x346dn57h",
    "https://scholarsphere.psu.edu/files/x346dn58s",
    "https://scholarsphere.psu.edu/files/x346dn592",
    "https://scholarsphere.psu.edu/files/x346dn60t",
    "https://scholarsphere.psu.edu/files/x346dn613",
    "https://scholarsphere.psu.edu/files/x346dn62c",
    "https://scholarsphere.psu.edu/files/x346dn63n",
    "https://scholarsphere.psu.edu/files/x346dn64x",
    "https://scholarsphere.psu.edu/files/x346dn65",
    "http://osf.io/share9"
]


def update_deleted_documents(apps, schema_editor):
    # Takes strings, lieral evals them into python Dicts
    PushedData = apps.get_model("push_endpoint", "PushedData")
    for item in PushedData.objects.all():
        if item.jsonData['uris']['providerUris'][0] in LIST_OF_DOCIDS:
            item.status = 'deleted'
            item.save()


class Migration(migrations.Migration):

    dependencies = [
        ('push_endpoint', '0023_dict_string'),
    ]

    operations = [
        migrations.RunPython(update_deleted_documents),
    ]
