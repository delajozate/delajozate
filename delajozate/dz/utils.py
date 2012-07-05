import datetime
from temporal import END_OF_TIME

from django.core.cache import cache

from django.contrib.contenttypes.models import ContentType
from dz.models import Mandat, Funkcija, ClanStranke, ClanOdbora, Oseba, Stranka, Pozicija, DrzavniZbor

#LONG_LIVE = 60*60*24 # Cache for a day
LONG_LIVE = 5 # 5 seconds cache

def null_date(date):
	if date == END_OF_TIME:
		return None
	return date
	

def get_mandat_current():
	cache_key = 'dz-mandat-current'
	mandat = cache.get(cache_key, 0)
	if not mandat:
		mandat = Mandat.objects.order_by('-st')[0]
		cache.set(cache_key, mandat, LONG_LIVE)
	return mandat
	

def get_poslanci_by_mandat(mandat=None):
	if not mandat:
		mandat = get_mandat_current()
	cache_key = 'dz-poslanci-mandat-%s' % ("%d" % mandat.st if mandat else "current")
	poslanci = cache.get(cache_key, [])
	if not poslanci:
		poslanci = Funkcija.objects.filter(mandat__st=mandat.st).select_related("oseba")
		#dz = DrzavniZbor.objects.get(mandat=mandat)
		#poslanci = Pozicija.objects.filter(tip_organizacije=ContentType.objects.get_for_model(dz), id_organizacije=dz.id)
		cache.set(cache_key, poslanci)
	return poslanci
	

def get_poslanec_stats(k, mandat=None, today=None):
	"""
	k = Funkcija
	"""
	if not mandat:
		mandat = get_mandat_current()
	if not today:
		today = datetime.date.today()
	kandidat = {}
	
	# ... osebne podatke (ime, sliko)
	oseba = k.oseba
	kandidat['oseba'] = oseba
	
	# ... mandate v katerih je bil (=> izracunaj stevilo in obdobje v dneh)
	mandati = Funkcija.objects.filter(oseba=oseba).select_related("mandat")
	
	kandidat['mandati'] = mandati
	kandidat['poslanskih_dni'] = sum([ ((null_date(m.do) or today) - m.od).days for m in mandati ])
	
	# ... stranke v katerih je bil
	clanstva = ClanStranke.objects.filter(oseba=oseba).select_related("stranka").order_by('-od') # ne -do, ker potem dobis predzadnjo!
	kandidat['stranke'] = set([n.stranka for n in clanstva])
	if clanstva:
		kandidat['stranka'] = clanstva[0].stranka
	
	# ... stevilo odborov v zadnjem mandatu
	odbori = set([])
	for pos_mandat in mandati:
		if pos_mandat.mandat == mandat:
			for clanstvo in ClanOdbora.objects.filter(poslanec__id=pos_mandat.id, mandat__id=mandat.id).select_related("odbor"):
				odbori.add(clanstvo.odbor.pk)
	kandidat['odbori'] = len(odbori)
	
	'''
	# ... stevilo komisij v zadnjem mandatu
	
	# ... stevilo delegacij v zadnjem mandatu
	'''
	
	return kandidat
	

def get_osebe_data():
	"""
	Vraca tuple dveh dictov:
	- osebe_mandati_dict (k = oseba.pk, v = set(Mandat))
	- osebe_dni (k = oseba.pk, v = int [stevilo dni kot poslanec]) 
	"""
	cache_key = 'dz-funkcije-mandat-%s' % str(datetime.date.today())
	osebe_data = cache.get(cache_key, None)
	if not osebe_data:
		today = datetime.date.today()
		osebe_dni_dict = {}
		osebe_mandati_dict = {}
		for funkcija in Funkcija.objects.all():
			pk = funkcija.oseba_id
			dni = osebe_dni_dict.setdefault(pk, 0)
			osebe_dni_dict[pk] = dni + ((null_date(funkcija.do) or today) - funkcija.od).days
			mandat = osebe_mandati_dict.setdefault(pk, set())
			mandat.add(funkcija.mandat)
		osebe_data = (osebe_mandati_dict, osebe_dni_dict)
		cache.set(cache_key, osebe_data)
	return osebe_data
	

def get_poslanci(filters=None, mandat=None):
	if not filters:
		filters = {}
	
	# mandati & dnevi / osebo
	osebe_mandati_dict, osebe_dni_dict =  get_osebe_data()
	
	# vsi clani, oseba samo prvic, clanstvo torej zadnje
	poslanci = []
	existing = set([])
	for clanstvo in ClanStranke.objects.filter(**filters).select_related('oseba', 'stranka').order_by('oseba__priimek', 'oseba__ime', '-od'):
		oseba = clanstvo.oseba
		pk = oseba.pk
		if pk not in existing:
			if not mandat or mandat in osebe_mandati_dict[pk]:
				poslanci.append({
					'oseba': oseba,
					'stranka': clanstvo.stranka,
					'poslanskih_dni': osebe_dni_dict[pk],
					'mandati': osebe_mandati_dict[pk],
					'short': True
				})
		existing.add(pk)
	
	return poslanci
	
