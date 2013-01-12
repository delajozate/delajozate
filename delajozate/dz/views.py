import collections
import datetime
import json

from django.http import HttpResponse
from django.shortcuts import render

import dz.news
from dz.models import Stranka, Oseba, Mandat, Tweet, Pozicija
from magnetogrami.models import Zasedanje, Glas, Glasovanje

from temporal import END_OF_TIME

def home(request):
	context = {
		'zasedanja': Zasedanje.objects.all().select_related('seja').order_by('-datum')[:15],
		'glasovanja': Glasovanje.objects.all().order_by('-datum')[:15],
	}
	return render(request, 'home.html', context)

def poslanci_list(request, mandat):
	if mandat == 'danes':
		poslanci = Pozicija.objects.filter(tip='poslanec', do=END_OF_TIME).order_by('oseba')
		mandat_str = 'today'
	else:
		mandat = mandat[:-len('-mandat')]
		m = Mandat.objects.get(st=mandat)
		mandat_str = '%s-mandat' % m.st,
		poslanci = Pozicija.objects.filter(tip='poslanec', organizacija__drzavnizbor__mandat=m).order_by('od', 'oseba')
	context = {
		'poslanci': poslanci,
		'mandat': mandat_str,
		'mandati': Mandat.objects.all(),
	}
	return render(request, 'poslanci.html', context)


def d_squared(tracks, nodepairs):
	#for a,b in nodepairs:
		#(tracks[a]-tracks[b])**2

	return list(sorted([((tracks[a] - tracks[b]) ** 2, a, b) for a, b in nodepairs], reverse=True))


def stranke_json(request):
	"json strank za d3.js vizualizacijo"

	stiki = {}

	for s in Stranka.objects.all().order_by('od'):
		start_sticisce = stiki.setdefault(s.od, {})
		start_sticisce.setdefault('od', []).append(s)
		end_sticisce = stiki.setdefault(s.do, {})
		end_sticisce.setdefault('do', []).append(s)

	masters = {}
	steze = {}
	povezave = {}
	stiki_list = list(sorted(stiki.items()))
	for k, s in stiki_list:
		if len(s.get('od', [])) == 1 and len(s.get('do', [])) == 1:
			# preimenovanje
			s_v = s['od'][0]
			s_iz = s['do'][0]
			mastr = masters.setdefault(s_iz.id, s_iz.id)
			while mastr != masters[mastr]:
				mastr = masters[mastr]
			masters[s_v.id] = mastr
			steze.setdefault(mastr, [s_iz]).append(s_v)
		elif len(s.get('od', [])) + len(s.get('do', [])) > 2:
			for d in s.get('od', []):
				do = povezave.setdefault(d.id, [])
				do.extend([i.id for i in s.get('do', [])])

	for s in Stranka.objects.all().order_by('od'):
		if not s.id in masters:
			steza = masters.setdefault(s.id, s.id)
			steze.setdefault(steza, [s])

	povezave_resolved = []
	for k, v in povezave.items():
		for i in v:
			povezave_resolved.append((masters[k], masters[i]))

	steze_index = dict([(b, a) for a, b in list(enumerate(steze.keys()))])

	stranke = {}
	for s in Stranka.objects.all():
		s_dict = {
			'id': s.id,
			'od': (s.od.year, s.od.month, s.od.day),
			'do': (s.do.year, s.do.month, s.do.day),
			'ime': s.ime,
			'okrajsava': s.okrajsava,
			'barva': s.barva,
			'nastala_iz': [i.id for i in s.nastala_iz.all()],
			'spremenila_v': [v.id for v in s.spremenila_v.all()],
			}
		stranke[s.id] = s_dict
	
	condensed = {}
	for master_id, steza in steze.iteritems():
		newsteza = []
		for s in steza:
			s_dict = {
			'id': s.id,
			'od': (s.od.year, s.od.month, s.od.day),
			'do': (s.do.year, s.do.month, s.do.day),
			'ime': s.ime,
			'okrajsava': s.okrajsava,
			'barva': s.barva,
			'nastala_iz': [i.id for i in s.nastala_iz.all()],
			'spremenila_v': [v.id for v in s.spremenila_v.all()],
			}
			newsteza.append(s_dict)
		condensed[master_id] = newsteza
	
	return HttpResponse(json.dumps({'stranke_all': stranke, 'stranke_condensed': condensed}, indent=3), mimetype='application/json')


def poslanec(request, slug):
	oseba = Oseba.objects.get(slug=slug)
	tweeti = Tweet.objects.filter(oseba=oseba)
	glasovi = Glas.objects.filter(oseba=oseba).select_related('glasovanje', 'glasovanje__seja')

	now = datetime.datetime.now()
	today = now.replace(hour=0, minute=0, second=0, microsecond=0)
	# TODO: actually count weeks
	this_week = now - datetime.timedelta(days=-7)
	last_week = now - datetime.timedelta(days=-14)
	two_weeks_ago = now - datetime.timedelta(days=-21)
	month_ago = now - datetime.timedelta(days=-31)

	casovnica = []
	for tweet in tweeti:
		casovnica.append((tweet.created_at, tweet, 'tweet'))
	for glas in glasovi:
		if glas.glasovanje.datum is not None:
			# convert date to datetime so we can compare it to datetime
			casovnica.append((datetime.datetime(*(glas.glasovanje.datum.timetuple()[:6])), glas, 'glas'))

	novice = dz.news.get_news(" ".join([oseba.ime, oseba.priimek]))
	if novice:
		for novica in novice:
			casovnica.append((novica["published"], novica, 'novica'))

	casovnica = sorted(casovnica, key=lambda k: k[0], reverse=True)

	context = {
		'oseba': oseba,
		'today_list': [],
		'this_week_list': [],
		'last_week_list': [],
		'two_weeks_ago_list': [],
		'month_ago_list': [],
		'the_rest_list': [],
	}

	item = collections.namedtuple('Item', 'obj, type')

	for date, obj, type_ in casovnica:
		if today < date <= now:
			context['today_list'].append(item._make((obj, type_)))
		if this_week < date <= today:
			context['this_week_list'].append(item._make((obj, type_)))
		if last_week < date <= this_week:
			context['last_week_list'].append(item._make((obj, type_)))
		if two_weeks_ago < date <= last_week:
			context['two_weeks_ago_list'].append(item._make((obj, type_)))
		if month_ago < date <= last_week:
			context['month_ago_list'].append(item._make((obj, type_)))
		if date <= month_ago:
			context['the_rest_list'].append(item._make((obj, type_)))

	return render(request, "poslanec.html", context)


def robots(request):

	robots_txt = """User-agent: *
Disallow: /iskanje/
"""

	return HttpResponse(robots_txt, mimetype="text/plain")
