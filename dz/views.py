from django.http import HttpResponse
from django.template import RequestContext, Context, loader
from django.core.cache import cache

from models import Mandat, Poslanec
from temporal import END_OF_TIME

import random, datetime

#LONG_LIVE = 60*60*24 # Cache for a day
LONG_LIVE = 5 # 5 seconds cache

def null_date(date):
	if date == END_OF_TIME:
		return None
	return date

def home(request):
	ctx = {}
	template = loader.get_template('home.html')
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
		poslanci = Poslanec.objects.filter(mandat=mandat)
		cache.set('dz-poslanci', poslanci)

	# Izberi 4 nakljucne
	st_poslancev = len(poslanci)
	picked = set([])
	izbrani = []
	while len(picked) < 4:
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
		k_mandati = Poslanec.objects.filter(oseba=oseba)

		kandidat['st_mandatov'] = len(k_mandati)
		dolzina_sluzenja = sum([ ((null_date(m.do) or today) - m.od).days for m in k_mandati ])
		kandidat['dolzina_sluzenja'] = dolzina_sluzenja

		'''
		# ... stranko v kateri je

		# ... stevilo strank v katerih je bil

		# ... stevilo odborov

		# ... stevilo komisij

		# ... stevilo delegacij
		'''
		izbrani.append(kandidat)

	ctx['izbrani'] = izbrani

	return HttpResponse(template.render(Context(ctx)))


def poslanec(request, slug):
	# Poberi poslanca s tem slugom

	# Poberi podatke zanj

	# Izpisi template 
	pass
