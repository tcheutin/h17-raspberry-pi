# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-18 21:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MobileCommuncationLog',
            new_name='MobileComsLog',
        ),
    ]
