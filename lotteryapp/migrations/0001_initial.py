# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lottery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hash_key', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('title', models.CharField(max_length=500)),
                ('registration_deadline', models.DateTimeField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Lottery',
                'verbose_name_plural': 'Lotteries',
            },
        ),
        migrations.CreateModel(
            name='LotteryParticipant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hash_key', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('email', models.EmailField(max_length=254)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('entry_code', models.CharField(max_length=10, blank=True)),
                ('is_winner', models.BooleanField(default=False)),
                ('registerd', models.DateTimeField(auto_now_add=True)),
                ('lottery', models.ForeignKey(to='lotteryapp.Lottery')),
            ],
            options={
                'verbose_name': 'Lottery Participant',
                'verbose_name_plural': 'Lottery Participants',
            },
        ),
        migrations.AddField(
            model_name='lottery',
            name='winner',
            field=models.ForeignKey(related_name='lottery_winner', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='lotteryapp.LotteryParticipant', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='lotteryparticipant',
            unique_together=set([('email', 'entry_code')]),
        ),
    ]
