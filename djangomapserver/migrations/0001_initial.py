# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClassObj',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('expression', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DataStoreBase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LayerObj',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('layer_type', models.SmallIntegerField(choices=[(3, b'raster'), (2, b'vector polygon'), (1, b'vector line'), (0, b'vector point')])),
                ('projection', models.CharField(default=b'init=epsg:4326', help_text=b'PROJ4 definition of the layer projection', max_length=255)),
                ('data', models.CharField(help_text=b'Full filename of the spatial data to process.', max_length=255)),
                ('class_item', models.CharField(help_text=b'Item name in attribute table to use for class lookups.', max_length=255, blank=True)),
                ('ows_abstract', models.TextField(blank=True)),
                ('ows_enable_request', models.CharField(default=b'*', max_length=255)),
                ('ows_include_items', models.CharField(default=b'all', max_length=50, blank=True)),
                ('gml_include_items', models.CharField(default=b'all', max_length=50, blank=True)),
                ('ows_opaque', models.SmallIntegerField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MapLayer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.SmallIntegerField(choices=[(0, b'off'), (1, b'on'), (2, b'default')])),
                ('layer_obj', models.ForeignKey(to='djangomapserver.LayerObj')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MapObj',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Unique identifier.', max_length=255)),
                ('status', models.SmallIntegerField(choices=[(0, b'off'), (1, b'on'), (2, b'default')])),
                ('projection', models.CharField(default=b'init=epsg:4326', help_text=b'PROJ4 definition of the map projection', max_length=255)),
                ('units', models.SmallIntegerField(blank=True, choices=[(5, b'Decimal degrees')])),
                ('size', models.CommaSeparatedIntegerField(help_text=b'Map size in pixel units', max_length=10)),
                ('cell_size', models.FloatField(help_text=b'Pixel size in map units.', null=True, blank=True)),
                ('image_type', models.CharField(max_length=10, choices=[(b'png', b'png')])),
                ('ows_sld_enabled', models.BooleanField(default=True)),
                ('ows_abstract', models.TextField(blank=True)),
                ('ows_enable_request', models.CharField(default=b'*', max_length=255)),
                ('ows_encoding', models.CharField(default=b'utf-8', max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MapServerColor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('red', models.IntegerField(null=True, blank=True)),
                ('green', models.IntegerField(null=True, blank=True)),
                ('blue', models.IntegerField(null=True, blank=True)),
                ('hex_string', models.CharField(max_length=9, blank=True)),
                ('attribute', models.CharField(max_length=255, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RectObj',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('max_x', models.FloatField()),
                ('max_y', models.FloatField()),
                ('min_x', models.FloatField()),
                ('min_y', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ShapefileDataStore',
            fields=[
                ('datastorebase_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='djangomapserver.DataStoreBase')),
                ('path', models.CharField(help_text=b'Path to the directory holding shapefiles.', max_length=255)),
            ],
            options={
            },
            bases=('djangomapserver.datastorebase',),
        ),
        migrations.CreateModel(
            name='SpatialiteDataStore',
            fields=[
                ('datastorebase_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='djangomapserver.DataStoreBase')),
                ('path', models.CharField(help_text=b'Path to the Spatialite database file.', max_length=255)),
            ],
            options={
            },
            bases=('djangomapserver.datastorebase',),
        ),
        migrations.CreateModel(
            name='StyleObj',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('class_obj', models.ForeignKey(to='djangomapserver.ClassObj')),
                ('color', models.ForeignKey(to='djangomapserver.MapServerColor')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='mapobj',
            name='extent',
            field=models.ForeignKey(help_text=b"Map's spatial extent.", to='djangomapserver.RectObj'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mapobj',
            name='image_color',
            field=models.ForeignKey(blank=True, to='djangomapserver.MapServerColor', help_text=b'Initial map background color.', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mapobj',
            name='layers',
            field=models.ManyToManyField(to='djangomapserver.LayerObj', null=True, through='djangomapserver.MapLayer', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='maplayer',
            name='map_obj',
            field=models.ForeignKey(to='djangomapserver.MapObj'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='maplayer',
            name='style',
            field=models.ForeignKey(blank=True, to='djangomapserver.StyleObj', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='layerobj',
            name='data_store',
            field=models.ForeignKey(to='djangomapserver.DataStoreBase'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='layerobj',
            name='extent',
            field=models.ForeignKey(help_text=b"Layer's spatial extent.", to='djangomapserver.RectObj'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='classobj',
            name='layer_obj',
            field=models.ForeignKey(to='djangomapserver.LayerObj'),
            preserve_default=True,
        ),
    ]
