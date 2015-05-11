from django.core.management.base import BaseCommand, CommandError
from indexsite.models import rssfeeds, usersrss
from datetime import timedelta
from django.utils import timezone

class Command(BaseCommand):
    help = 'Update RSS feeds'
    def handle(self, *args, **options):
        five_minutes_ago = timezone.now()-timedelta(minutes=5) 
        g = rssfeeds.objects.filter(rssupdatetime__lt=five_minutes_ago)[:10]
        for n in g:
            if usersrss.objects.filter(feed=n).count() > 0:
                n.remove_last()
                n.get_news()
                n.rssupdatetime = timezone.now()
                n.save()
            else:
                n.delete()