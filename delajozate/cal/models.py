# -*- coding: utf-8 -*-

import re
import datetime

from django.db import models

class Event(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    location = models.CharField(max_length=500)
    title = models.CharField(max_length=2000)
    category = models.CharField(max_length=500)
    url = models.CharField(max_length=1000, blank=True, null=True)
    note = models.CharField(max_length=2000)
    vir = models.CharField(max_length=100)
    
URL = 'http://192.168.33.126:8001/drzava/dzrs/urnik/?id__gte=%s'

def fetch_dzrs_events():
    import requests
    n = 0
    resp = requests.get(URL % n)
    
    for day in resp.json():
        for e in day['json']:
            notes = e.get('opomba', '')
            dtkw = re.match('(?P<year>\d{4})-(?P<month>\d\d)-(?P<day>\d\d)', e['date']).groupdict()
            try:
                d = re.search('(?P<hour>\d\d):(?P<minute>\d\d)', e['time']).groupdict()
            except:
                d = {'hour': '8', 'minute': '00'}
                notes = (notes + ' ' + e['time']).strip()
            
            dtkw.update(d)
            dtkw = dict([(k,int(v)) for k,v in dtkw.iteritems()])

            start = datetime.datetime(**dtkw)
            end = start + datetime.timedelta(hours=1)
            
            if len(Event.objects.filter(title=e.get('title'), start=start))>0:
                continue
            
            event = Event()
            event.start = start
            event.end = end
            event.location = u"Državni zbor - " + (e.get('location') if e.get('location') is not None else "")
            event.title = e.get('title')
            event.url  = e.get('url')
            event.note = notes
            event.category = u"Državni zbor - " + e.get('tip_dogodka_text')
            event.vir = "DZRS"
            event.save()

