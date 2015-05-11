# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('indexsite', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rssfeeds',
            name='rssupdatetime',
            field=models.DateTimeField(verbose_name='Updating time', default=datetime.datetime(2014, 12, 11, 14, 58, 54, 873179, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='key_expires',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 11, 14, 58, 54, 878617, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
