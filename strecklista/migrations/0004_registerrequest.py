# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-19 13:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('strecklista', '0003_auto_20170220_1247'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegisterRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('message', models.TextField(blank=True, max_length=500)),
            ],
        ),
    ]
