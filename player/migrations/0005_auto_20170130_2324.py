# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-31 04:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0004_song_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='username',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='song',
            unique_together=set([('artist', 'title', 'account')]),
        ),
    ]