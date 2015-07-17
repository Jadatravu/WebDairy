# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AcademicYear',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('academic_year', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('H_No', models.CharField(max_length=30)),
                ('Line1', models.CharField(max_length=30)),
                ('street', models.CharField(max_length=30)),
                ('colony', models.CharField(max_length=30)),
                ('city', models.CharField(max_length=30)),
                ('pin', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('sur_name', models.CharField(max_length=30)),
                ('login_name', models.CharField(default='suser1', max_length=30)),
                ('email', models.EmailField(max_length=75)),
                ('emp_id', models.IntegerField()),
                ('phone', models.IntegerField()),
                ('picture', models.FileField(upload_to='tmp/')),
                ('ac_year', models.ManyToManyField(to='modelsapp.AcademicYear')),
                ('address', models.OneToOneField(to='modelsapp.Address')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('dep_name', models.CharField(max_length=30)),
                ('class_teacher_id', models.IntegerField(default=0)),
                ('ac_year', models.ManyToManyField(to='modelsapp.AcademicYear')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Holiday',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('h_date', models.DateField()),
                ('holiday_name', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='JobTitle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Leave',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('app_id', models.IntegerField(default=0)),
                ('req_date', models.DateField(default=datetime.datetime.now)),
                ('app_date', models.DateField(default=datetime.datetime.now)),
                ('from_date', models.DateField(default=datetime.datetime.now)),
                ('to_date', models.DateField(default=datetime.datetime.now)),
                ('count', models.IntegerField(default=0)),
                ('state', models.IntegerField(default=0)),
                ('type', models.IntegerField(default=0)),
                ('req_comment', models.CharField(default='-', max_length=250)),
                ('app_comment', models.CharField(default='-', max_length=250)),
                ('requester', models.ForeignKey(to='modelsapp.Contact')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LeaveBalance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('sick_leave_balance', models.IntegerField(default=0)),
                ('earned_leave_balance', models.IntegerField(default=0)),
                ('contact', models.OneToOneField(to='modelsapp.Contact')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('skill_name', models.CharField(max_length=30)),
                ('exp_years', models.IntegerField()),
                ('exp_level', models.IntegerField()),
                ('contact', models.ManyToManyField(to='modelsapp.Contact')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SkillTitle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('skill_title', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('sub_name', models.CharField(max_length=50)),
                ('teacher_id', models.IntegerField(default=0)),
                ('text_book', models.CharField(max_length=50)),
                ('publisher', models.CharField(max_length=50)),
                ('department_name', models.CharField(default='No deparment', max_length=50)),
                ('ac_year', models.ManyToManyField(to='modelsapp.AcademicYear')),
                ('department', models.ManyToManyField(to='modelsapp.Department')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Supervisor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('sup_id', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('test_name', models.CharField(max_length=50)),
                ('marks', models.IntegerField(default=0)),
                ('grade', models.CharField(max_length=50)),
                ('comment', models.CharField(max_length=500)),
                ('contact', models.ManyToManyField(to='modelsapp.Contact')),
                ('subject', models.ManyToManyField(to='modelsapp.Subject')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='supervisor',
            unique_together=set([('sup_id',)]),
        ),
        migrations.AlterUniqueTogether(
            name='subject',
            unique_together=set([('sub_name', 'text_book', 'publisher', 'department_name')]),
        ),
        migrations.AlterUniqueTogether(
            name='skilltitle',
            unique_together=set([('skill_title',)]),
        ),
        migrations.AlterUniqueTogether(
            name='jobtitle',
            unique_together=set([('title',)]),
        ),
        migrations.AlterUniqueTogether(
            name='department',
            unique_together=set([('dep_name',)]),
        ),
        migrations.AddField(
            model_name='contact',
            name='department',
            field=models.ManyToManyField(to='modelsapp.Department'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contact',
            name='job_title',
            field=models.ForeignKey(to='modelsapp.JobTitle'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contact',
            name='supervisor',
            field=models.ForeignKey(to='modelsapp.Supervisor'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='contact',
            unique_together=set([('first_name', 'last_name', 'sur_name')]),
        ),
        migrations.AlterUniqueTogether(
            name='academicyear',
            unique_together=set([('academic_year',)]),
        ),
    ]
