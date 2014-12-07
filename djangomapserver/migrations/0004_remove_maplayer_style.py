# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangomapserver', '0003_classobj_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='maplayer',
            name='style',
        ),
    ]
