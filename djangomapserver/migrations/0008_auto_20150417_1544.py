# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangomapserver', '0007_rasterdatastore'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rasterdatastore',
            options={'verbose_name': 'Raster Datastore'},
        ),
        migrations.AlterModelOptions(
            name='shapefiledatastore',
            options={'verbose_name': 'Shapefile Datastore'},
        ),
        migrations.AlterModelOptions(
            name='spatialitedatastore',
            options={'verbose_name': 'Spatialite Datastore'},
        ),
    ]
