from django.db import models
from datetime import datetime, timedelta
from django.utils import timezone
import feedparser
from django.contrib.auth.models import User

class rssfeeds(models.Model):
    isfeed = models.BooleanField('Is feed correct', default=False)
    feedaddress = models.URLField('Feed url', help_text='Write url of rss feed', unique=True, blank=True)
    version = models.CharField('Version of RSS', max_length=200, default="blank", blank=True)
    rsstitle = models.CharField('Channel title', max_length=200, default="blank", blank=True)
    rssdescription = models.TextField('Channel description', default="blank", blank=True)
    rssupdatetime = models.DateTimeField('Updating time', default=timezone.now())
    def __str__(self):
        return u"%s" % (self.rsstitle)
    def save(self, *args, **kwargs):
        rssdata = feedparser.parse(self.feedaddress)
        if rssdata['bozo'] == 0:
            self.isfeed = True
        else:
            self.isfeed = False
        self.version = rssdata['version']
        self.rsstitle = rssdata['channel']['title']
        self.rssdescription = rssdata['channel']['description']
        self.rssupdatetime = self.rssupdatetime
        super(rssfeeds, self).save(*args, **kwargs)
    def get_news(self):
        feed = feedparser.parse(self.feedaddress)
        count_add = 0
        for i in feed['items']:
            try:
                correst_date = str(i['published_parsed'][2])+" "+str(i['published_parsed'][1])+" "+str(i['published_parsed'][0])+" "+str(i['published_parsed'][3])+":"+str(i['published_parsed'][4])+":"+str(i['published_parsed'][5])
                correst_date = datetime.strptime(correst_date, '%d %m %Y %H:%M:%S')
                correst_date = timezone.make_aware(correst_date, timezone.get_current_timezone())
                if rssnews.objects.filter(newsdate=correst_date,newstitle=i['title'],rssfeed=self).exists():
                    pass
                else:
                    try:
                        fulltext = i['fulltext']
                    except:
                        try:
                            fulltext = i['summary']
                        except:
                            fulltext = ""
                    it = rssnews(rssfeed=self, newsdate=correst_date, newstitle=i['title'], newstext=fulltext, newslink=i['link'])
                    it.save()
                    usersnews = usersrss.objects.filter(feed=self)
                    for usr in usersnews:
                        unreadnews = usernews(user=usr.user,usernew=it,isread=False)
                        unreadnews.save()
                    count_add=count_add+1
            except Exception as inst:
                print(type(inst))
                print(inst)
        return count_add
    def remove_last(self):
        thee_days_ago = timezone.now()-timedelta(days=3) 
        news = rssnews.objects.filter(newsdate__lt=thee_days_ago)
        for new in news:
            usersnews = usernews.objects.filter(usernew=new)
            usersnews.delete()
        news.delete()
    class Meta:
        verbose_name_plural=u'RSS feeds'

class rssnews(models.Model):
    rssfeed = models.ForeignKey('rssfeeds', limit_choices_to={'isfeed': True})
    newsdate = models.DateTimeField('Date')
    newstitle = models.CharField('Title', max_length=200)
    newstext = models.TextField('Text')
    newslink = models.URLField('Link')
    def __str__(self):
        return u"%s" % (self.newstitle)
    def get_rssfeed(self):
        return u"%s" % (self.rssfeed.rsstitle)
    class Meta:
        verbose_name_plural=u'News'

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(default=timezone.now())
    def __str__(self):
        return u"%s" % (self.user.username)
    class Meta:
        verbose_name_plural=u'User profiles'

class usersrss(models.Model):
    user = models.ForeignKey(User)
    feed = models.ForeignKey('rssfeeds', limit_choices_to={'isfeed': True})
    def __str__(self):
        return u"%s - %s" % (self.user.username, self.feed.rsstitle)
    def save(self, *args, **kwargs):
        news = rssnews.objects.filter(rssfeed=self.feed)[:10]
        for new in news:
            unreadnews = usernews(user=self.user,usernew=new,isread=False)
            unreadnews.save()
        super(usersrss, self).save(*args, **kwargs)
    def delete(self, *args, **kwargs):
        rssid = self.feed.id
        rss_news = usernews.objects.select_related("rssnews").filter(usernew__rssfeed__id=rssid)
        rss_news.delete()
        super(usersrss, self).delete(*args, **kwargs)
    class Meta:
        verbose_name_plural=u'Users and they RSS channels'

class usernews(models.Model):
    user = models.ForeignKey(User)
    usernew = models.ForeignKey(rssnews)
    isread = models.BooleanField(default=False)
    def __str__(self):
        return u"%s - %s" % (self.user.username, self.usernew.newstitle)
    class Meta:
        verbose_name_plural=u'Users and they news'