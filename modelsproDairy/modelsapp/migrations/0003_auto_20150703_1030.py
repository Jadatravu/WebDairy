# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('modelsapp', '0002_academicyear_current'),
    ]

    operations = [
        migrations.AlterField(
            model_name='academicyear',
            name='current',
            field=models.BooleanField(),
        ),
    ]
