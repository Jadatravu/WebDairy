# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('modelsapp', '0003_auto_20150703_1030'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='academic_year',
            field=models.ManyToManyField(to='modelsapp.AcademicYear'),
        ),
        migrations.AlterField(
            model_name='academicyear',
            name='current',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
