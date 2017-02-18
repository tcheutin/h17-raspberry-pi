# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-18 21:39
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mobile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('token', models.CharField(max_length=30)),
                ('ipAddress', models.CharField(max_length=30, null=True)),
                ('status', models.CharField(max_length=30)),
                ('loginTime', models.DateTimeField(default=datetime.date.today)),
                ('logoutTime', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MobileCommuncationLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('httpResponse', models.IntegerField()),
                ('mobileId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Mobile')),
            ],
        ),
        migrations.CreateModel(
            name='Terminal',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('Connected', 'Connected'), ('Non-Responsive', 'Non-Responsive')], default='Connected', max_length=30)),
                ('ipAddress', models.CharField(max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticketHash', models.CharField(default=None, max_length=30, unique=True)),
                ('status', models.CharField(choices=[('Validated', 'Validated'), ('Non-Validated', 'Non-Validated'), ('In Progress', 'In Progress')], default='Non-Validated', max_length=30)),
                ('validationTime', models.DateTimeField()),
                ('validationTerminal', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Terminal')),
            ],
        ),
        migrations.AddField(
            model_name='mobilecommuncationlog',
            name='ticketId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Ticket'),
        ),
    ]
