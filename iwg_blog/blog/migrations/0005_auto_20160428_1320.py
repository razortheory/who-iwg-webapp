# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-28 13:20
from __future__ import unicode_literals

from django.db import migrations
import iwg_blog.utils.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20160426_1025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='tags',
            field=iwg_blog.utils.models.fields.OrderedManyToManyField(blank=True, related_name='articles', to='blog.Tag'),
        ),
    ]
