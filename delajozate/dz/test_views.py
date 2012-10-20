from django.test import TestCase
from django.test.client import RequestFactory

from dz.views import poslanec


class PoslanecTest(TestCase):

    def setUp(self):
        self.request_factory = RequestFactory()

    def test_foo(self):
        resp = poslanec(request.factory.get('/osebe/dragutin-mate/'), 'dragutin-mate')
        import pdb; pdb.set_trace()
