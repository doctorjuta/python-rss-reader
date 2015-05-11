from django.contrib import admin
from django.contrib.auth.models import User
from indexsite.models import rssfeeds, rssnews, usersrss, usernews
from indexsite.forms import rssnewsAdminForm, usersrssAdminForm

class defaultUser(admin.ModelAdmin):
    list_display=('username',)
admin.site.unregister(User)
admin.site.register(User,defaultUser)

class rssfeedsadmin(admin.ModelAdmin):
    list_display=('rsstitle','feedaddress')
admin.site.register(rssfeeds,rssfeedsadmin)

class rssnewsAdmin(admin.ModelAdmin):
    list_display=('newstitle','getrssfeed','newsdate',)
    list_filter=('rssfeed__rsstitle',)
    ordering=('-newsdate',)
    form = rssnewsAdminForm
    def getrssfeed(self, obj):
        return obj.rssfeed.rsstitle
    getrssfeed.short_description = 'Source'
admin.site.register(rssnews, rssnewsAdmin)

class usersrssAdmin(admin.ModelAdmin):
    form = usersrssAdminForm
admin.site.register(usersrss, usersrssAdmin)
admin.site.register(usernews)