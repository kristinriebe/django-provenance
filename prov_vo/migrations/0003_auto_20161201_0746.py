# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-12-01 07:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('prov_vo', '0002_agent_wasassociatedwith_wasattributedto'),
    ]

    operations = [
        migrations.CreateModel(
            name='WasGeneratedByDescription',
            fields=[
                ('id', models.CharField(max_length=128, primary_key=True, serialize=False)),
                ('role', models.CharField(blank=True, max_length=128, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='wasgeneratedby',
            name='role',
        ),
        migrations.AddField(
            model_name='activity',
            name='docuLink',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='documentation link'),
        ),
        migrations.AddField(
            model_name='activity',
            name='parametervalues',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='activitydescription',
            name='parametertypes',
            field=models.CharField(blank=True, max_length=2048, null=True),
        ),
        migrations.AlterField(
            model_name='activitydescription',
            name='docuLink',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='documentation link'),
        ),
        migrations.AddField(
            model_name='wasgeneratedbydescription',
            name='activitydescription',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='prov_vo.ActivityDescription'),
        ),
        migrations.AddField(
            model_name='wasgeneratedbydescription',
            name='entitydescription',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='prov_vo.EntityDescription'),
        ),
        migrations.AddField(
            model_name='wasgeneratedby',
            name='description',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='prov_vo.WasGeneratedByDescription'),
        ),
    ]