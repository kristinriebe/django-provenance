# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-12-01 08:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prov_vo', '0003_auto_20161201_0746'),
    ]

    operations = [
        migrations.RenameField(
            model_name='agent',
            old_name='label',
            new_name='name',
        ),
    ]
