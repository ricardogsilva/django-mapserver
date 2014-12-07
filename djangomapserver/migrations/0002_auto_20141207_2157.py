# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangomapserver', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='layerobj',
            name='data',
            field=models.CharField(help_text=b'Full path to the spatial data to process.', max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='layerobj',
            name='projection',
            field=models.PositiveSmallIntegerField(default=4326, help_text=b'EPSG code of the layer projection'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mapobj',
            name='projection',
            field=models.PositiveSmallIntegerField(default=4326, help_text=b'EPSG code of the map projection'),
            preserve_default=True,
        ),
    ]
