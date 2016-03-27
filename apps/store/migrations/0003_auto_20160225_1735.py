# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-25 17:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20160214_0934'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='orderstatus',
            options={'verbose_name_plural': 'Order statuses'},
        ),
        migrations.AlterModelOptions(
            name='productstatus',
            options={'verbose_name_plural': 'Product statuses'},
        ),
        migrations.RemoveField(
            model_name='category',
            name='parentCategory',
        ),
        migrations.AddField(
            model_name='category',
            name='parentCategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.Category'),
        ),
    ]
