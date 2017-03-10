# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-10 21:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20170310_2044'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mobilecommlog',
            name='terminalId',
        ),
        migrations.RemoveField(
            model_name='mobilecommlog',
            name='ticketId',
        ),
        migrations.AddField(
            model_name='mobilecommlog',
            name='ticketHash',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='mobilecommlog',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
