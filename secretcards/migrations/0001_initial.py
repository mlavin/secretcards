# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import simpleflake
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('uid', models.BigIntegerField(default=simpleflake.simpleflake, unique=True, db_index=True)),
                ('message', models.TextField()),
                ('image', models.CharField(choices=[('blue-eyes.png', 'sue_salisbury-maui-hawaii'), ('nose.png', 'comedynose'), ('black.png', '11638547@N00'), ('pair.png', 'crsan'), ('flying.png', 'sadie_16'), ('looking-up.png', 'albaraa'), ('gray.pnp', 'mtrichardson'), ('three.png', 'londonlooks')], max_length=200)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
