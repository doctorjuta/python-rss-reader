# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='rssfeeds',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('isfeed', models.BooleanField(verbose_name='Is feed correct', default=False)),
                ('feedaddress', models.URLField(help_text='Write url of rss feed', unique=True, verbose_name='Feed url', blank=True)),
                ('version', models.CharField(max_length=200, verbose_name='Version of RSS', blank=True, default='blank')),
                ('rsstitle', models.CharField(max_length=200, verbose_name='Channel title', blank=True, default='blank')),
                ('rssdescription', models.TextField(verbose_name='Channel description', blank=True, default='blank')),
                ('rssupdatetime', models.DateTimeField(verbose_name='Updating time', default=datetime.datetime(2014, 12, 10, 18, 1, 30, 656297, tzinfo=utc))),
            ],
            options={
                'verbose_name_plural': 'RSS feeds',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='rssnews',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('newsdate', models.DateTimeField(verbose_name='Date')),
                ('newstitle', models.CharField(max_length=200, verbose_name='Title')),
                ('newstext', models.TextField(verbose_name='Text')),
                ('newslink', models.URLField(verbose_name='Link')),
                ('rssfeed', models.ForeignKey(to='indexsite.rssfeeds')),
            ],
            options={
                'verbose_name_plural': 'News',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='usernews',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('isread', models.BooleanField(default=False)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('usernew', models.ForeignKey(to='indexsite.rssnews')),
            ],
            options={
                'verbose_name_plural': 'Users and they news',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('activation_key', models.CharField(max_length=40, blank=True)),
                ('key_expires', models.DateTimeField(default=datetime.datetime(2014, 12, 10, 18, 1, 30, 661587, tzinfo=utc))),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'User profiles',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='usersrss',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('feed', models.ForeignKey(to='indexsite.rssfeeds')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Users and they RSS channels',
            },
            bases=(models.Model,),
        ),
    ]
