
import unittest
import os

from django.test import Client, TestCase

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
        
