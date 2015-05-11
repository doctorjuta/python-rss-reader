from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from indexsite.models import rssfeeds, UserProfile, usersrss, rssnews, usernews
from indexsite.forms import UserForm, usersrssAddForm
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import hashlib, random
from datetime import datetime, timedelta
from django.utils import timezone
from django.db import IntegrityError
from json import JSONEncoder

# Create your views here.

def register(request):
    args = {}
    args.update(csrf(request))
    args['registered'] = False
    if request.user.is_authenticated():
        return HttpResponseRedirect('/feed/read/')
    else:
        if request.method == 'POST':
            submittype = request.POST['submit']
            if submittype == 'Login':
                username = request.POST['username']
                password = request.POST['password']
                user = auth.authenticate(username=username,password=password)
                if user:
                    if user.is_active:
                        auth.login(request, user)
                        return HttpResponseRedirect('/feed/read/')
                    else:
                        return HttpResponse("Your account is disabled.")
                else:
                    print("Invalid login details: {0}, {1}".format(username,password))
                    return HttpResponse("Invalid login details supplied.")
            if submittype == 'Register':
                user_form = UserForm(request.POST)
                args['user_form'] = user_form
                if user_form.is_valid():
                    user_form.save()
                    username = user_form.cleaned_data['username']
                    email = user_form.cleaned_data['email']
                    salt = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:5]
                    activation_key = hashlib.sha1(salt.encode('utf-8')+email.encode('utf-8')).hexdigest()
                    key_expires = timezone.now()+timedelta(days=2)
                    user = User.objects.get(username=username)
                    new_profile = UserProfile(user=user,activation_key=activation_key,key_expires=key_expires)
                    new_profile.save()
                    email_subject = "Account confirmation"
                    email_body = "Hey %s, thanks for signing up. To activate your account, click this link within 48 hours http://127.0.0.1:8000/feed/confirm/%s" % (username,activation_key)
                    try:
                        send_mail(email_subject,email_body,'no-replay@some.com',[email],fail_silently=False)
                    except:
                        print("Problem with connection to smtp server")
                    args['registered'] = True
                else:
                    print(user_form.errors)
        else:
            args['user_form'] = UserForm()
    return render_to_response   ('indexsite/register.html', args, context_instance=RequestContext(request))

def register_confirm(request, activation_key):
    args = {}
    if request.user.is_authenticated():
        HttpResponseRedirect('/feed')
    user_profile = get_object_or_404(UserProfile,activation_key=activation_key)
    if user_profile.key_expires < timezone.now():
        return render_to_response('indexsite/confirm_expired.html', args, context_instance=RequestContext(request))
    user = user_profile.user
    user.is_active = True
    user.save()
    return render_to_response('indexsite/confirm.html', args, context_instance=RequestContext(request))

@login_required
def user_logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/feed/')

@login_required
def read(request):
    args = {}
    return render_to_response('indexsite/read.html', args, context_instance=RequestContext(request))

@login_required
def loadread(request):
    args = {}
    all_news = usernews.objects.select_related('rssnews').filter(user=request.user).order_by('-usernew__newsdate')
    all_news_paged = Paginator(all_news, 25)
    page_c = int(request.POST["page_c"])
    try:
        args['usernews'] = all_news_paged.page(page_c)
    except PageNotAnInteger:
        pass
    except EmptyPage:
        args['nomorepage'] = "1"
    return render_to_response('indexsite/read_news.html', args, context_instance=RequestContext(request))

@login_required
def makeread(request):
    pass

@login_required
def rsslist(request):
    args = {}
    args['userfeeds'] = usersrss.objects.filter(user=request.user)
    if request.method == 'POST':
        try:
            somev = request.POST['submit_rss']
            newrss = usersrssAddForm(request.POST)
            if newrss.is_valid():
                rss_feed = newrss.cleaned_data['rssfeed']
                newrssObj = rssfeeds(feedaddress=rss_feed)
                valit_rss_feed = True
                try:
                    newrssObj.save()
                except KeyError:
                    args['message'] = "You give invalide RSS feed. Try to add another."
                    valit_rss_feed = False
                except IntegrityError:
                    newrssObj = rssfeeds.objects.get(feedaddress=rss_feed)
                if valit_rss_feed:
                    usersfeed = usersrss(user=request.user, feed=newrssObj)
                    try:
                        usersfeed.save()
                        args['message'] = "New rss feed added to your list."
                    except IntegrityError:
                        args['message'] = "Sorry, but this feed is already in your list. Try to add another."
            else:
                args['message'] = "Form is not valid. Please enter correct RSS feed link."
        except:
            try:
                rss_id = request.POST['remove']
                rssuser = usersrss.objects.get(feed__id=rss_id)
                rssuser.delete()
                args['message'] = 'RSS channel was removed successfully'
            except:
                args['message'] = 'We have some problem with operating your request. Please, contact with admins.'
    args['addrssform'] = usersrssAddForm()
    return render_to_response('indexsite/rsslist.html', args, context_instance=RequestContext(request))