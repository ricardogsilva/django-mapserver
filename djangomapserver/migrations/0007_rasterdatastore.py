# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangomapserver', '0006_auto_20150414_2307'),
    ]

    operations = [
        migrations.CreateModel(
            name='RasterDataStore',
            fields=[
                ('datastorebase_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='djangomapserver.DataStoreBase')),
                ('path', models.CharField(help_text=b'Path to the directory holding raster files.', max_length=255)),
            ],
            options={
            },
            bases=('djangomapserver.datastorebase',),
        ),
    ]
