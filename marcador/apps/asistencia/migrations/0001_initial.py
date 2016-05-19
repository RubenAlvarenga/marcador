# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-18 22:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Asistencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entrada', models.DateTimeField(editable=False, verbose_name='Entrada')),
                ('salida', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='Salida')),
                ('user', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'ordering': ('entrada',),
                'verbose_name': 'Asistencia',
                'verbose_name_plural': 'Asistencias',
            },
        ),
    ]
