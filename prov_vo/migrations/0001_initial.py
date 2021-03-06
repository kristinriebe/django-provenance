# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-09-30 12:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.CharField(max_length=128, primary_key=True, serialize=False)),
                ('label', models.CharField(max_length=128, null=True)),
                ('startTime', models.DateTimeField(null=True)),
                ('endTime', models.DateTimeField(null=True)),
                ('annotation', models.CharField(blank=True, max_length=1024, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ActivityDescription',
            fields=[
                ('id', models.CharField(max_length=128, primary_key=True, serialize=False)),
                ('label', models.CharField(max_length=128, null=True)),
                ('type', models.CharField(choices=[('cs:simulation', 'cs:simulation'), ('cs:processing', 'cs:processing')], max_length=128, null=True)),
                ('subtype', models.CharField(blank=True, choices=[('cs:halofinding', 'cs:halofinding'), ('cs:mergertree-generation', 'cs:mergertree-generation'), ('cs:substructuretree-generation', 'cs:substructuretree-generation')], max_length=128, null=True)),
                ('description', models.CharField(blank=True, max_length=1024, null=True)),
                ('docuLink', models.CharField(blank=True, max_length=512, null=True, verbose_name='documentation link')),
            ],
        ),
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.CharField(max_length=128, primary_key=True, serialize=False)),
                ('label', models.CharField(max_length=128, null=True)),
                ('type', models.CharField(max_length=128, null=True)),
                ('location', models.CharField(max_length=128, null=True)),
                ('access', models.CharField(max_length=128, null=True)),
                ('size', models.CharField(max_length=128, null=True)),
                ('format', models.CharField(max_length=128, null=True)),
                ('annotation', models.CharField(blank=True, max_length=1024, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EntityDescription',
            fields=[
                ('id', models.CharField(max_length=128, primary_key=True, serialize=False)),
                ('label', models.CharField(max_length=128, null=True)),
                ('description', models.CharField(blank=True, max_length=1024, null=True)),
                ('docuLink', models.CharField(blank=True, max_length=512, null=True, verbose_name='documentation link')),
                ('dataproduct_type', models.CharField(max_length=128, null=True)),
                ('dataproduct_subtype', models.CharField(max_length=128, null=True)),
                ('level', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Used',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('activity', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='prov_vo.Activity')),
            ],
        ),
        migrations.CreateModel(
            name='UsedDescription',
            fields=[
                ('id', models.CharField(max_length=128, primary_key=True, serialize=False)),
                ('role', models.CharField(blank=True, max_length=128, null=True)),
                ('activitydescription', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='prov_vo.ActivityDescription')),
                ('entitydescription', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='prov_vo.EntityDescription')),
            ],
        ),
        migrations.CreateModel(
            name='WasGeneratedBy',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('role', models.CharField(blank=True, max_length=128, null=True)),
                ('activity', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='prov_vo.Activity')),
                ('entity', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='prov_vo.Entity')),
            ],
        ),
        migrations.AddField(
            model_name='used',
            name='description',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='prov_vo.UsedDescription'),
        ),
        migrations.AddField(
            model_name='used',
            name='entity',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='prov_vo.Entity'),
        ),
        migrations.AddField(
            model_name='entity',
            name='description',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='prov_vo.EntityDescription'),
        ),
        migrations.AddField(
            model_name='activity',
            name='description',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='prov_vo.ActivityDescription'),
        ),
    ]
