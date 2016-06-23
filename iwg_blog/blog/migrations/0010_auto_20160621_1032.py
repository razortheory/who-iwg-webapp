# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-21 08:32
from __future__ import unicode_literals

import django
from django.db import migrations, models


def migrate_category(apps, schema_editor):
    Article = apps.get_model('blog', 'Article')

    for article in Article.objects.all():
        article.categories = [article.category]


def migrate_category_backward(apps, schema_editor):
    Article = apps.get_model('blog', 'Article')

    for article in Article.objects.all():
        article.category = article.categories.first()
        article.save()


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_articledocument'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='articles', to='blog.Category'),
        ),
        migrations.AddField(
            model_name='article',
            name='categories',
            field=models.ManyToManyField(related_name='articles', to='blog.Category'),
        ),
        migrations.RunPython(
            migrate_category,
            migrate_category_backward,
        ),
        migrations.RemoveField(
            model_name='article',
            name='category',
        ),
    ]