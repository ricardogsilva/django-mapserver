# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djangomapserver.validators


class Migration(migrations.Migration):

    dependencies = [
        ('djangomapserver', '0005_auto_20141207_2254'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostgisDataStore',
            fields=[
                ('datastorebase_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='djangomapserver.DataStoreBase')),
                ('database', models.CharField(help_text=b'Database name.', max_length=255)),
                ('user', models.CharField(help_text=b'Database user name.', max_length=255)),
                ('password', models.CharField(help_text=b'Database user password.', max_length=255)),
                ('host', models.CharField(default=b'localhost', help_text=b'Database host address.', max_length=255)),
                ('port', models.IntegerField(default=5432, help_text=b'Database host listening port.')),
            ],
            options={
                'verbose_name': 'PostGIS Datastore',
            },
            bases=('djangomapserver.datastorebase',),
        ),
        migrations.AlterField(
            model_name='mapobj',
            name='units',
            field=models.SmallIntegerField(choices=[(5, b'Decimal degrees')]),
        ),
        migrations.AlterField(
            model_name='mapservercolor',
            name='blue',
            field=models.IntegerField(blank=True, null=True, validators=[djangomapserver.validators.validate_integer_color]),
        ),
        migrations.AlterField(
            model_name='mapservercolor',
            name='green',
            field=models.IntegerField(blank=True, null=True, validators=[djangomapserver.validators.validate_integer_color]),
        ),
        migrations.AlterField(
            model_name='mapservercolor',
            name='hex_string',
            field=models.CharField(blank=True, max_length=9, validators=[djangomapserver.validators.validate_hex_color]),
        ),
        migrations.AlterField(
            model_name='mapservercolor',
            name='red',
            field=models.IntegerField(blank=True, null=True, validators=[djangomapserver.validators.validate_integer_color]),
        ),
    ]
