# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangomapserver', '0002_auto_20141207_2157'),
    ]

    operations = [
        migrations.AddField(
            model_name='classobj',
            name='name',
            field=models.CharField(default='replace me', max_length=50),
            preserve_default=False,
        ),
    ]
