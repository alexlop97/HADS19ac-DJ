# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-05-14 14:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20180514_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='correct_choice',
            field=models.IntegerField(),
        ),
    ]
