# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-14 15:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmailUser', '0002_myuser_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='is_Hedda_Hopper',
            field=models.BooleanField(default=False),
        ),
    ]
