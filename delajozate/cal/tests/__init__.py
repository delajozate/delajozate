"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import Client, TestCase
import os
import json

def data_file(x):
    return os.path.join(os.path.dirname(__file__), x)

class CalendarTest(TestCase):
    def test_responses(self):
        c = Client()
        resp = c.get('/koledar/ical/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp['content-type'], 'text/calendar')
        
        from delajozate.cal.models import parse_dzrs_events
        j = json.load(open(data_file('events_dzrs.json')))
        parse_dzrs_events(j)

        resp = c.get('/koledar/ical/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp['content-type'], 'text/calendar')
        
