# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import simpleflake


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('uid', models.BigIntegerField(default=simpleflake.simpleflake, db_index=True, unique=True)),
                ('message', models.TextField()),
                ('image', models.CharField(choices=[('blue-eyes.png', 'sue_salisbury-maui-hawaii'), ('nose.png', 'comedynose'), ('black.png', '11638547@N00'), ('pair.png', 'crsan'), ('flying.png', 'sadie_16'), ('looking-up.png', 'albaraa'), ('gray.pnp', 'mtrichardson'), ('three.png', 'londonlooks')], max_length=200)),
                ('username', models.CharField(max_length=255)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
