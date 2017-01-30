# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-29 22:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0002_auto_20170127_1934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='latitude',
            field=models.DecimalField(decimal_places=6, default=-48.876667, max_digits=9),
        ),
        migrations.AlterField(
            model_name='account',
            name='longitude',
            field=models.DecimalField(decimal_places=6, default=-123.393333, max_digits=9),
        ),
        migrations.AlterField(
            model_name='song',
            name='latitude',
            field=models.DecimalField(decimal_places=6, default=-48.876667, max_digits=9),
        ),
        migrations.AlterField(
            model_name='song',
            name='longitude',
            field=models.DecimalField(decimal_places=6, default=-123.393333, max_digits=9),
        ),
    ]