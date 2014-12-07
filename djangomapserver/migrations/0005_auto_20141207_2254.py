# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangomapserver', '0004_remove_maplayer_style'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classobj',
            name='expression',
            field=models.CharField(max_length=255, blank=True),
            preserve_default=True,
        ),
    ]
