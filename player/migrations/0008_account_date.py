# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-03 21:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0007_auto_20170201_1949'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
