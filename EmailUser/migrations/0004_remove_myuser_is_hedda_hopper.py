# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-06 09:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('EmailUser', '0003_myuser_is_hedda_hopper'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='is_Hedda_Hopper',
        ),
    ]
