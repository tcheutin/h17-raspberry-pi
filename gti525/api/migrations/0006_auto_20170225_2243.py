# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-25 22:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20170221_0444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mobile',
            name='status',
            field=models.CharField(choices=[('Connected', 'Connected'), ('Non-Responsive', 'Non-Responsive')], default='Connected', max_length=30),
        ),
        migrations.AlterField(
            model_name='terminal',
            name='status',
            field=models.CharField(choices=[('Connected', 'Connected'), ('Non-Responsive', 'Non-Responsive')], default='Connected', max_length=30),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.CharField(choices=[('Validated', 'Validated'), ('Non-Validated', 'Non-Validated'), ('In Progress', 'In Progress')], default='Non-Validated', max_length=30),
        ),
    ]
