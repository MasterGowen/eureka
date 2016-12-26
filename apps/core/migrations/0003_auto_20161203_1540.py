# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-03 09:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20161126_1927'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='unreg_email',
            field=models.EmailField(blank=True, max_length=30, verbose_name='Email for answer unregistered user'),
        ),
        migrations.AddField(
            model_name='bid',
            name='unreg_phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128),
        ),
        migrations.AlterField(
            model_name='bid',
            name='author',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Author'),
        ),
    ]
