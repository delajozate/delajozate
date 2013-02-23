import os
import datetime

from django.test import Client, TestCase
from django.test.client import RequestFactory

from dz.views import poslanec
from dz.models import Tweet, Oseba


class DZTest(TestCase):
    fixtures = [
        os.path.join(os.path.dirname(__file__), '../fixtures/delajozate.json')
    ]

    def setUp(self):
        self.c = Client()

    def test_responses(self):
        resp = self.c.get('/')
        self.assertEqual(resp.status_code, 200)

        resp = self.c.get('/poslanci/')
        self.assertEqual(resp.status_code, 301)

        resp = self.c.get('/poslanci/danes/')
        self.assertEqual(resp.status_code, 200)

        resp = self.c.get('/poslanci/3-mandat/')
        self.assertEqual(resp.status_code, 200)

        resp = self.c.get('/osebe/borut-ambrozic/')
        self.assertEqual(resp.status_code, 200)

        resp = self.c.get('/seje/')
        self.assertEqual(resp.status_code, 200)

        resp = self.c.get('/iskanje/')
        self.assertEqual(resp.status_code, 200)

        resp = self.c.get('/robots.txt')
        self.assertEqual(resp.status_code, 200)

        resp = self.c.get('/glasovanja/')
        self.assertEqual(resp.status_code, 200)


class PoslanecTest(TestCase):
    #fixtures = [
        #os.path.join(os.path.dirname(__file__), '../fixtures/delajozate.json'),
        #os.path.join(os.path.dirname(__file__), '../fixtures/seja_glasovanje_glas.json'),
    #]

    def setUp(self):
        self.c = Client()
        oseba = Oseba(slug="dragutin-mate", ime='Dragutin', priimek='Mate')
        oseba.save()
        self.tweet1 = Tweet.objects.create(text='July', oseba=oseba, tweet_id=1, created_at=datetime.datetime.now()-datetime.timedelta(32))
        self.tweet2 = Tweet.objects.create(text='August', oseba=oseba, tweet_id=2, created_at=datetime.datetime.now()-datetime.timedelta(31))

    def test_order(self):
        resp = self.c.get('/osebe/dragutin-mate/tweets/')
        self.assertEqual(resp.context['object_list'][0], self.tweet2)
        #self.assertEqual(resp.context['the_rest_list'][1].obj.glasovanje.datum, datetime.date(2012, 7, 13))
        
        self.assertEqual(resp.context['object_list'][1], self.tweet1)
        #self.assertEqual(len(resp.context['the_rest_list']), 18)
