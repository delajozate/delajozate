from django.http import HttpResponse
from django.shortcuts import render
from dz.utils import get_poslanci, get_mandat_current

from dz.models import Funkcija, Stranka, Oseba, Mandat
from magnetogrami.models import Zasedanje

import json
from delajozate.temporal import END_OF_TIME

POSLANCI_RANDOM_LIMIT = 4

def home(request):
	context = {
		'zasedanja': Zasedanje.objects.all().order_by('-datum')[:5]
	}
	
	return render(request, 'home.html', context)
	

def stranka(request, stranka_id):
	ctx = {
		'poslanci': get_poslanci({'stranka__pk': stranka_id}, mandat=get_mandat_current()),
	}
	return render(request, 'poslanci.html', ctx)
	

def poslanci_list(request, mandat):
	if mandat == 'danes':
		poslanci = Funkcija.objects.filter(funkcija='poslanec', do=END_OF_TIME).order_by('oseba__priimek')
		mandat_str = 'today'
	else:
		mandat = mandat[:-len('-mandat')]
		m = Mandat.objects.get(st=mandat)
		mandat_str = '%s-mandat' % m.st,
		poslanci = Funkcija.objects.filter(funkcija='poslanec', od__gte=m.od, do__lte=m.do).order_by('oseba__priimek')
	context = {
		'poslanci': poslanci,
		'mandat': mandat_str,
		'mandati': Mandat.objects.all(),
	}
	return render(request, 'poslanci.html', context)
	

def d_squared(tracks, nodepairs):
	#for a,b in nodepairs:
		#(tracks[a]-tracks[b])**2
		
	return list(sorted([((tracks[a]-tracks[b])**2,a,b) for a,b in nodepairs], reverse=True))
	

def stranke_json(request):
	"json strank za d3.js vizualizacijo"
	
	stiki = {}
	
	for s in Stranka.objects.all().order_by('od'):
		start_sticisce = stiki.setdefault(s.od, {})
		start_sticisce.setdefault('od', []).append(s)
		end_sticisce = stiki.setdefault(s.do, {})
		end_sticisce.setdefault('do', []).append(s)
	
	from pprint import pprint
	
	masters = {}
	steze = {}
	povezave = {}
	stiki_list = list(sorted(stiki.items()))
	for k, s in stiki_list:
		#print s
		if len(s.get('od', [])) == 1 and len(s.get('do', [])) == 1:
			# preimenovanje
			s_v  = s['od'][0]
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
	
	steze_index = dict([(b,a) for a,b in list(enumerate(steze.keys()))])
	
	#pprint(steze)
	
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
	context = {
		'oseba': Oseba.objects.get(slug=slug),
		}
	
	return render(request, "poslanec.html", context)

def robots(request):
	
	robots_txt = """User-agent: *
Disallow: /iskanje/
"""
	
	return HttpResponse(robots_txt, mimetype="text/plain")

def gplus_racuni(request):
	from delajozate.dz.social import get_all_gplus_account_candidates
	osebe = get_all_gplus_account_candidates()
	ctx = { "osebe" : osebe }
	return render(request, "gplus_racuni.html", ctx)

def gplus_racuni_submit(request):
	for oseba_id, plus_id in request.POST.items():
		if not oseba_id.isdigit() or not plus_id.isdigit():
			continue

		if int(plus_id) == 0:
			continue

		oseba = Oseba.objects.get(pk=int(oseba_id))
		oseba.google_plus = plus_id
		oseba.save()
		print oseba.ime, oseba.priimek, "-", plus_id

	return HttpResponse("OK")