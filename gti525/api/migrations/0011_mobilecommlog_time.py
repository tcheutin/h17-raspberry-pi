# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-10 21:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20170310_2100'),
    ]

    operations = [
        migrations.AddField(
            model_name='mobilecommlog',
            name='time',
            field=models.DateTimeField(null=True),
        ),
    ]
