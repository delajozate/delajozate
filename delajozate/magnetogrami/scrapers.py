import re
import lxml.html
import datetime
import requests

from delajozate.magnetogrami.models import Video

EXTID_DZ = 85927166
EXTID_DT = 85927167

URL = 'http://tvslo.si/?c_mod=play&op=search&func=search&ignore=&search_text=&search_media=tv&search_type=&search_extid=%s&search_orderby=date&search_order=desc&search_dateframe=1m&search_datefrom=&search_dateto=%s&page=0'


def parse_video_html(data):
	if isinstance(data, unicode):
		data = data.encode('raw_unicode_escape')
	d = lxml.html.fromstring(data)
	d.make_links_absolute('http://tvslo.si/')
	parsed = []
	for tr in d.xpath('//table/tr'):
		tds = tr.xpath('.//td')
		video_page_url = ''
		title = ''
		
		a = tds[0].xpath('.//a')
		if a:
			a = a[0]
			video_page_url = a.attrib.get('href')
			title = a.attrib.get('title')
		else:
			#print lxml.html.tostring(tr)
			continue
		datum = tds[1].xpath('.//text()')[0]
		if title is None:
			continue
		if datum:
			datum = datetime.datetime.strptime(datum, '%d.%m.%Y')
		info = {
			'video_page_url': video_page_url, 
			'title': title.encode('raw_unicode_escape').decode('utf-8'),
			'datum': datum,
		}
		parsed.append(info)
	return parsed

def save_videos(parsed):
	for vinfo in parsed:
		m = re.search('/(ava\d\.\d+)/', vinfo['video_page_url'])
		if not m:
			raise Exception('could not save video, no ava? %s' % vinfo)
		ava_id = m.group(1)
		v, created = Video.objects.get_or_create(url=vinfo['video_page_url'], title=vinfo['title'], datum=vinfo['datum'], ava_id=ava_id)
		v.save()

def fetch_video_html():
	date = datetime.datetime.now().strftime('%d.%m.%Y')
	for i in [EXTID_DZ, EXTID_DT]:
		url = URL % (i, date)
		try:
			resp = requests.get(url)
			yield resp
		except Exception, e:
			print e

def run_videos():
	for resp in fetch_video_html():
		videos = parse_video_html(resp.content)
		save_videos(videos)
