import json
import re
import datetime

from django.db import models

class Event(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    location = models.CharField(max_length=500)
    title = models.CharField(max_length=500)
    category = models.CharField(max_length=500)
    url = models.CharField(max_length=1000)
    note = models.CharField(max_length=2000)
    vir = models.CharField(max_length=100)

URL = 'http://localhost:8001/drzava/dzrs/urnik/?id__gte=%s'

from pprint import pprint

def fetch_dzrs_events():
    import requests
    n = 0
    resp = requests.get(URL % n)
    
    for day in resp.json():
        print day['json']
        for e in day['json']:
            print 'event!'
            pprint(e)
            
            notes = e.get('opomba', '')
            dtkw = re.match('(?P<year>\d{4})-(?P<month>\d\d)-(?P<day>\d\d)', e['date']).groupdict()
            print e['time']
            try:
                d = re.search('(?P<hour>\d\d):(?P<minute>\d\d)', e['time']).groupdict()
            except:
                d = {'hour': '8', 'minute': '00'}
                notes = (notes + ' ' + e['time']).strip()
            
            dtkw.update(d)
            dtkw = dict([(k,int(v)) for k,v in dtkw.iteritems()])
            print dtkw
            start = datetime.datetime(**dtkw)
            end = start + datetime.timedelta(3600)
            
            #ev = Event(start=)
            
        
