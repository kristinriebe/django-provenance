# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-12-01 08:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prov_vo', '0004_auto_20161201_0802'),
    ]

    operations = [
        migrations.RenameField(
            model_name='agent',
            old_name='description',
            new_name='affiliation',
        ),
    ]
