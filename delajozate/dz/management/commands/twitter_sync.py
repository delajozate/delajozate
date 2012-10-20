import datetime

import twitter
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import NoArgsCommand

from delajozate.dz.models import Tweet
from delajozate.dz.models import Oseba


class Command(NoArgsCommand):
	help = "Sync twitter feeds"

	def handle_noargs(self, **options):
		# see http://pypi.python.org/pypi/python-twitter/0.8.2
		# https://dev.twitter.com/docs/api/1.1/get/lists/statuses
		api = twitter.Api()
		osebe = Oseba.objects.exclude(twitter='').exclude(twitter=None).all()
		for oseba in osebe:
			tweets = api.GetUserTimeline(oseba.twitter, count=10000, include_rts=False)
			for tweet in tweets:
				try:
					# TODO: get_or_create
					t = Tweet.objects.get(tweet_id=tweet.id)
				except ObjectDoesNotExist:
					t = Tweet(tweet_id=tweet.id, text=tweet.text)
					t.created_at = datetime.datetime.utcfromtimestamp(tweet.created_at_in_seconds)
					t.oseba = oseba
					t.save()
