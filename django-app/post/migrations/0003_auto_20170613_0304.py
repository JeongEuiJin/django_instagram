# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-13 03:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_auto_20170612_1252'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='create_date',
            new_name='created_date',
        ),
        migrations.RenameField(
            model_name='commentlike',
            old_name='create_date',
            new_name='created_date',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='create_date',
            new_name='created_date',
        ),
        migrations.RenameField(
            model_name='postlike',
            old_name='create_date',
            new_name='created_date',
        ),
    ]