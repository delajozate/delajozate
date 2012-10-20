from django.core.cache import cache
from dz.models import Oseba
import requests

GPLUS_APIKEY = "AIzaSyBdE_P4t5zIY0xm8G02ym6yigLN1_uwG0M"
GPLUS_SEARCH_ENDPOINT = "https://www.googleapis.com/plus/v1/people/"

def get_all_gplus_account_candidates():
	"""
	Runs a search over Google+ API for all "Oseba" and returns potential matches
	"""

	cached_result = cache.get("gplus_accounts")
	if cached_result:
		return cached_result

	results = {}

	for oseba in Oseba.objects.all():
		print "=== %s %s" % (oseba.ime, oseba.priimek)

		params = {u"query": u"%s %s" % (oseba.ime, oseba.priimek, ), u"key" : GPLUS_APIKEY}
		response = requests.get(GPLUS_SEARCH_ENDPOINT, params=params)
		if len(response.json["items"]) == 0:
			continue

		oseba_plus = []
		for result_item in response.json["items"]:
			search_result = {}
			search_result["plus_name"] = result_item["displayName"]
			img_url = result_item["image"]["url"]
			search_result["plus_img"] = img_url[:img_url.find("?sz=")]
			search_result["plus_id"] = result_item["id"]
			oseba_plus.append(search_result)
		results[oseba] = oseba_plus

	cache.set("gplus_accounts", results)
	return results