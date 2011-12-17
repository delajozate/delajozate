from django.http import HttpResponse
from django.template import RequestContext, Context, loader
from django.core.cache import cache
from django.shortcuts import render_to_response

from models import Mandat, Funkcija, ClanOdbora, ClanStranke, Stranka
from temporal import END_OF_TIME

import datetime
import json
import random

#LONG_LIVE = 60*60*24 # Cache for a day
LONG_LIVE = 5 # 5 seconds cache

def null_date(date):
	if date == END_OF_TIME:
		return None
	return date

def home(request):
	ctx = {}
	
	today = datetime.date.today()

	mandat = None
	mandat_st = cache.get('dz-aktualni-mandat', 0)
	if not mandat:
		mandat = Mandat.objects.order_by('-st')[0]
		mandat_st = mandat.st
		cache.set('dz-zadnji-mandat', mandat_st, LONG_LIVE)

	# Malo poslancev na mandat, zato poberi vse za random izbor
	poslanci = cache.get('dz-poslanci', [])
	if not poslanci:
		if not mandat:
			mandat = Mandat.objects.filter(st=mandat_st)[0]
		poslanci = Funkcija.objects.filter(mandat=mandat)
		cache.set('dz-poslanci', poslanci)

	# Izberi 4 nakljucne
	st_poslancev = len(poslanci)
	picked = set([])
	izbrani = []
	while len(picked) < 8:
		picked.add(poslanci[random.randint(0, st_poslancev-1)])

	# Za vsakega kandidata poberi...
	for k in picked:
		kandidat = {}

		# ... osebne podatke (ime, sliko)
		oseba = k.oseba
		kandidat['ime'] = "%s %s" % (oseba.ime, oseba.priimek)
		kandidat['slug'] = oseba.slug
		kandidat['slika'] = oseba.slika

		# ... mandate v katerih je bil (=> izracunaj stevilo in obdobje v dneh)
		k_mandati = Funkcija.objects.filter(oseba=oseba)

		kandidat['st_mandatov'] = len(k_mandati)
		dolzina_sluzenja = sum([ ((null_date(m.do) or today) - m.od).days for m in k_mandati ])
		kandidat['dolzina_sluzenja'] = dolzina_sluzenja
		
		poslanske_skupine = list(ClanStranke.objects.filter(oseba=oseba).order_by('-do'))
		if poslanske_skupine:
			kandidat['stranka'] = poslanske_skupine[0]
		kandidat['stevilo_strank'] = len(poslanske_skupine)
		
		'''
		# ... stranko v kateri je

		# ... stevilo strank v katerih je bil
		'''

		# ... stevilo odborov v zadnjem mandatu
		odbori = set([])
		pos_mandati = Funkcija.objects.filter(oseba=oseba, mandat=mandat) # e.g.: poslanec->minister->poslanec
		for pos_mandat in pos_mandati:
			for clanstvo in ClanOdbora.objects.filter(poslanec=pos_mandat, mandat=mandat):
				odbori.add(clanstvo.odbor.pk)
		kandidat['odbori'] = len(odbori)

		'''
		# ... stevilo komisij v zadnjem mandatu

		# ... stevilo delegacij v zadnjem mandatu
		'''
		izbrani.append(kandidat)

	ctx['izbrani'] = izbrani
	return render_to_response('home.html', Context(ctx))

def poslanci_list(request):
	clanstvo = list(ClanStranke.objects.all().select_related('oseba', 'stranka').order_by('oseba__priimek', 'oseba__ime'))
	
	funkcije = Funkcija.objects.all().select_related('oseba', 'stranka')
	
	# stevilo dni
	today = datetime.date.today()
	dni_dict = {}
	mandatov = {}
	for f in funkcije:
		dni = dni_dict.setdefault(f.oseba.pk, 0)
		dni_dict[f.oseba.pk] = dni + ((null_date(f.do) or today) - f.od).days
		mandat = mandatov.setdefault(f.oseba.pk, set())
		mandat.add(f.mandat)
	
	for i in clanstvo:
		i.oseba.dni = dni_dict[i.oseba.pk]
		i.oseba.st_mandatov = len(mandatov[i.oseba.pk])
	
	context = {
		'object_list': clanstvo,
		}
	return render_to_response('dz/oseba_list.html', RequestContext(request, context))

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
	# Poberi poslanca s tem slugom

	# Poberi podatke zanj

	# Izpisi template 
	pass
