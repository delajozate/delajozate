"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase, Client
import os
here = lambda x: os.path.join(os.path.dirname(os.path.abspath(__file__)), x)


class MagnetogramiTest(TestCase):
    fixtures = [
        here('../../fixtures/delajozate.json'),
    ]
    
    def test_magnetogrami(self):
        import json
        from magnetogrami.models import seja_import_one
        
        j = json.load(open(here('test_seja.json')))
        print "importin' seja"
        seja_import_one(j['json'])
        
        c = Client()
        
        resp = c.get('/seje/')
        self.assertEqual(resp.status_code, 200)
        
        # TODO FIXME XXX
        #resp = c.get('/seje/5-mandat/')
        #self.assertEqual(resp.status_code, 200)
        
        resp = c.get('/seje/5-mandat/dz/')
        self.assertEqual(resp.status_code, 200)
        
        resp = c.get('/seje/5-mandat/dz/11-redna/')
        self.assertEqual(resp.status_code, 200)
        
        resp = c.get('/seje/5-mandat/dz/11-redna/2009-11-25/')
        self.assertEqual(resp.status_code, 200)
        
        