from dateutil.tz import tzlocal
import json
import urllib
import urllib2
import dateutil.parser
from django.conf import settings
from django.core.cache import cache

def get_news(topic):
    newsbuddy_url = settings.NEWSBUDDY_URL
    if not newsbuddy_url:
        return None

    results = cache.get(topic)
    if not results:
        try:
            url = "/".join([newsbuddy_url.rstrip("/"), "news/query/"])
            query = urllib2.urlopen("%s?%s"  % (url, urllib.urlencode({"q" : topic.encode("utf-8")}), ))
            news = json.loads(query.read())
        except urllib2.URLError:
            return None

        results = []
        for item in news["results"]:
            published = dateutil.parser.parse(item["published"])
            # Convert to TZ-naive representation
            published = published.astimezone(tzlocal()).replace(tzinfo=None)
            item["published"] = published
            results.append(item)

        cache.set(topic, results, 1800)    # Half and hour of caching
    return results