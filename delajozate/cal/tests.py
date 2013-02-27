"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import Client, TestCase


class CalendarTest(TestCase):
    def test_responses(self):
        c = Client()
        resp = c.get('/koledar/ical/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp['content-type'], 'text/calendar')

