# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-23 19:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20161223_1812'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='_timeleft',
        ),
    ]