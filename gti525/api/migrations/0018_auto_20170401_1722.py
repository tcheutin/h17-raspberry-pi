# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-01 17:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_delete_mobile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mobilecommlog',
            name='httpResponse',
            field=models.CharField(default='', max_length=30),
        ),
    ]