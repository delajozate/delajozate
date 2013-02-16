# coding: utf-8
import datetime
import time

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.shortcuts import render
from django.db import connection
from django.contrib.auth.decorators import login_required

from dz.models import Mandat, Oseba, Funkcija, DelovnoTelo, ClanOdbora, Pozicija
from magnetogrami.models import Glasovanje

VERBOSE = False

def _check_mandat():
	mandat_errors = []
	
	mandati = Mandat.objects.all().order_by('od', 'do')
	start = datetime.date(1992, 12, 23)
	for m in mandati:
		if m.od != start:
			mandat_errors.append(u'Mandat %s se začne z %s, pričakovano je bilo %s' % (m.st, m.od, start))
		start = m.do
	if start != datetime.date(9999, 12, 31):
		mandat_errors.append(u'Zadnji mandat se ne konča z 9999-12-31.')
	
	return mandat_errors

def _check_oseba():
	
	oseba_errors = []
	osebe = Oseba.objects.all()
	vseh_oseb = Oseba.objects.all().count()
	
	brez_slik = Oseba.objects.filter(slika='').count()
	if brez_slik > 0:
		oseba_errors.append('Brez slike je %s oseb (vseh je %s).' % (brez_slik, vseh_oseb))
	
	slike_brez_vira = Oseba.objects.filter(vir_slike='').exclude(slika='').count()
	if slike_brez_vira > 0:
		oseba_errors.append('%s slik nima navedenega vira.' % (slike_brez_vira, ))
	
	return oseba_errors

def _check_funkcija():
	funkcija_errors = []
	
	vseh_funkcij = Funkcija.objects.all().count()
	
	cur = connection.cursor()
	sql = """SELECT * FROM (SELECT F.id, F.oseba_id, OS.ime, OS.priimek, F.mandat_id, M.st, F.od, F.do, M.od, M.do, M.od <= F.od as spodnji_limit, M.do >= F.do as zgornji_limit from dz_funkcija F join dz_mandat M on (M.id=F.mandat_id) join dz_oseba OS on (OS.id=F.oseba_id)) AS Q where Q.spodnji_limit = false OR Q.zgornji_limit = false;"""
	cur.execute(sql, [])
	data = cur.fetchall()
	if data:
		ids = [i.id for i in data]
		funkcija_errors.append(u'Funkcije so zunaj meja mandatov: %s' % (ids))
	
	sql = """SELECT prevec_poslancev, COUNT(*) AS c, MIN(st_poslancev) AS najmanj, MAX(st_poslancev) AS najvec FROM (SELECT byday.datum, byday.st_poslancev, byday.st_poslancev > 90 AS prevec_poslancev FROM (SELECT datumi.datum, (SELECT COUNT(*) FROM dz_funkcija f WHERE f.funkcija='poslanec' AND f.od <= datumi.datum AND f.do > datumi.datum) AS st_poslancev FROM (SELECT '1992-12-23'::date + s.t AS datum FROM generate_series(0,(date_trunc('day', now())::date - '1992-12-23'::date)) AS s(t)) AS datumi) AS byday WHERE byday.st_poslancev <> 90) AS counter GROUP BY prevec_poslancev ORDER BY prevec_poslancev;"""
	cur.execute(sql, [])
	data = cur.fetchall()
	for row in data:
		funkcija_errors.append(u'Število dni, ko je %s kot 90 poslancev: %s (med %s in %s)' % (u"več" if row[0] else "manj", row[1], row[2], row[3]))

	sql = """select id from dz_funkcija where mandat_id is null;"""
	cur = connection.cursor()
	cur.execute(sql, [])
	data = cur.fetchall()
	if len(data):
		funkcija_errors.append(u'Število funkcij brez povezanega mandata: %s' % len(data))
		if VERBOSE:
			for row in data:
				funkcija_errors.append(u'- nima stranke: %s' % Funkcija.objects.filter(pk=row[0]).values()[0])
	
	sql = """select id from dz_funkcija where oseba_id is null;"""
	cur = connection.cursor()
	cur.execute(sql, [])
	data = cur.fetchall()
	if len(data):
		funkcija_errors.append(u'Število funkcij brez povezane osebe: %s' % len(data))
		if VERBOSE:
			for row in data:
				funkcija_errors.append(u'- nima osebe: %s' % Funkcija.objects.filter(pk=row[0]).values()[0])
	
	sql = """select count(*) c, oseba_id, min(id) from dz_funkcija where mandat_id is not null group by oseba_id, mandat_id, od, "do", opombe, podatki_preverjeni having count(*) > 1 order by c desc, oseba_id;"""
	cur = connection.cursor()
	cur.execute(sql, [])
	data = cur.fetchall()
	if len(data):
		funkcija_errors.append(u'Število duplikatov: %d (največje število kopij: %d)' % (len(data), data[0][0]))
		if VERBOSE:
			for row in data:
				funkcija_errors.append(u'- duplikat: %s' % Funkcija.objects.filter(pk=row[2]).values()[0])
	
	return funkcija_errors

def _check_delovnotelo():
	delovnotelo_errors = []
	
	sql = """SELECT * from (SELECT DT.id, DT.mandat_id, M.do, DT.od, DT.do, M.do = DT.do AND M.od = DT.od as date_check from dz_delovnotelo DT join dz_mandat M on (M.id=DT.mandat_id)) as Q where Q.date_check = false;"""
	cur = connection.cursor()
	cur.execute(sql, [])
	data = cur.fetchall()
	if data:
		ids = [i[0] for i in data]
		delovnotelo_errors.append(u'Delovna telesa nimajo pravilnih datumov glede na mandat: %s' % (ids))
	
	brez_idjev = DelovnoTelo.objects.filter(dz_id='')
	if brez_idjev.count() > 0:
		ids = [i.id for i in brez_idjev]
		delovnotelo_errors.append(u'Delovna telesa nimajo DZ_ID polj: %s' % (ids,))
	
	return delovnotelo_errors

def _check_seja():
	seja_errors = []
	
	sql = """SELECT * FROM (SELECT S.id, S.datum_zacetka, S.datum_zacetka >= M.od AND S.datum_zacetka <= M.do as datum_check from magnetogrami_seja S join dz_mandat M on (S.mandat=M.st)) AS Q WHERE Q.datum_check = false;"""
	cur = connection.cursor()
	cur.execute(sql, [])
	data = cur.fetchall()
	if data:
		ids = [i[0] for i in data]
		seja_errors.append(u'Datum pričetka seje ni znotraj časovnega okvira mandata: %s' % (ids,))
	
	return seja_errors

def _check_zasedanje():
	zasedanje_errors = []
	sql = """SELECT * FROM (SELECT S.id as seja_id, S.naslov as naslov_seje, S.mandat, Z.id as zasedanje_id, Z.datum as datum_zasedanja, M.od <= Z.datum AND M.do >= Z.datum as datum_check from magnetogrami_zasedanje Z join magnetogrami_seja S on (Z.seja_id=S.id) join dz_mandat M on (M.st=S.mandat)) AS Q WHERE Q.datum_check=false;"""
	cur = connection.cursor()
	cur.execute(sql, [])
	data = cur.fetchall()
	if data:
		ids = [i[0] for i in data]
		zasedanje_errors.append(u'Zasedanja datumsko niso znotraj pravega mandata: %s' % (ids,))
	
	sql = """SELECT count(*) from magnetogrami_zasedanje where url is null;"""
	cur.execute(sql, [])
	data = cur.fetchall()
	if data:
		zasedanje_errors.append(u'Število zasedanj, ki nimajo URLja na stran DZ: %s' % (data,))
	
	return zasedanje_errors

def _check_zapis():
	zapis_errors = []
	
	sql = """SELECT count(*) from (SELECT count(govorec), govorec from magnetogrami_zapis where govorec_oseba_id is null group by govorec) as q;"""
	
	cur = connection.cursor()
	cur.execute(sql, [])
	data = cur.fetchall()
	if data[0]:
		zapis_errors.append(u'Število različnih govorcev pri zapisih brez povezave govorca na osebo: %s' % (data[0],))
	
	return zapis_errors

def _check_glasovanje():
	glasovanje_errors = []
	
	vseh_glasovanj = Glasovanje.objects.all().count()
	glasovanja_brez_datuma = Glasovanje.objects.filter(datum=None).count()
	if glasovanja_brez_datuma > 0:
		glasovanje_errors.append(u'Brez datuma je %s glasovanj (vseh je %s).' % (glasovanja_brez_datuma, vseh_glasovanj))
	
	sql = """SELECT * FROM (SELECT G.id as glasovanje_id, seja_id, G.datum as datum_glasovanja, M.st as mandat, G.datum >= M.od AND G.datum <= M.do as datum_check from magnetogrami_glasovanje G join magnetogrami_seja S ON (S.id=G.seja_id) join dz_mandat M ON (M.st=S.mandat) where G.datum is not null) AS Q where Q.datum_check = false;"""
	cur = connection.cursor()
	cur.execute(sql, [])
	data = cur.fetchall()
	if data:
		ids = [i[0] for i in data]
		glasovanje_errors.append(u'Datum glasovanja ne ustreza mandatu seje: %s' % (ids,))
	
	sql = """SELECT * FROM (SELECT *, Q1.min_datum <= Q1.datum AND Q1.max_datum >= Q1.datum as datum_check FROM (SELECT G.id, G.datum, (SELECT min(datum) from magnetogrami_zasedanje where seja_id=G.seja_id) as min_datum, (SELECT max(datum) from magnetogrami_zasedanje where seja_id=G.seja_id) as max_datum from magnetogrami_glasovanje G join magnetogrami_seja S on (S.id=G.seja_id)) AS Q1) AS Q WHERE datum_check = false;"""
	cur = connection.cursor()
	cur.execute(sql, [])
	data = cur.fetchall()
	if data:
		ids = [i[0] for i in data]
		glasovanje_errors.append(u'Datum glasovanja ne ustreza zasedanjem seje: %s' % (ids,))
	
	sql = """SELECT count(*) FROM magnetogrami_glasovanje WHERE naslov = '';"""
	cur = connection.cursor()
	cur.execute(sql, [])
	data = cur.fetchall()
	if data:
		glasovanje_errors.append(u'Glasovanj brez naslova: %s' % data[0])
	
	return glasovanje_errors


def _check_glas():
	glas_errors = []
	
	sql = """SELECT count(*) from magnetogrami_glas where oseba_id is null;"""
	cur = connection.cursor()
	cur.execute(sql, [])
	data = cur.fetchall()
	if data[0]:
		glas_errors.append(u'Število glasov, ki nimajo povezave na osebo: %s' % (data[0],))
	
	return glas_errors

def _check_clanstranke():
	clanstranke_errors = []
	
	sql = """select id from dz_clanstranke where stranka_id is null;"""
	cur = connection.cursor()
	cur.execute(sql, [])
	data = cur.fetchall()
	if len(data):
		clanstranke_errors.append(u'Število članstev brez povezane stranke: %s' % len(data))
		if VERBOSE:
			for row in data:
				clanstranke_errors.append(u'- nima stranke: %s' % ClanStranke.objects.filter(pk=row[0]).values()[0])
	
	sql = """select id from dz_clanstranke where oseba_id is null;"""
	cur = connection.cursor()
	cur.execute(sql, [])
	data = cur.fetchall()
	if len(data):
		clanstranke_errors.append(u'Število članstev brez povezane osebe: %s' % len(data))
		if VERBOSE:
			for row in data:
				clanstranke_errors.append(u'- nima osebe: %s' % ClanStranke.objects.filter(pk=row[0]).values()[0])
	
	sql = """select count(*) c, oseba_id, min(id) from dz_clanstranke where stranka_id is not null group by oseba_id, stranka_id, od, "do", opombe, podatki_preverjeni having count(*) > 1 order by c desc, oseba_id;"""
	cur = connection.cursor()
	cur.execute(sql, [])
	data = cur.fetchall()
	if len(data):
		clanstranke_errors.append(u'Število duplikatov: %d (največje število kopij: %d)' % (len(data), data[0][0]))
		if VERBOSE:
			for row in data:
				clanstranke_errors.append(u'- duplikat: %s' % ClanStranke.objects.filter(pk=row[2]).values()[0])
	
	return clanstranke_errors
	

def _check_translation():
	# these only make sense before you migrate to 0024
	errors = []
	funkcije = Funkcija.objects.all().order_by("od", "do", "oseba__id")
	pozicija_dz = Pozicija.objects.filter(organizacija__drzavnizbor__gt=0)
	clanistranke = ClanStranke.objects.all().order_by("od", "do", "stranka__id", "oseba__id")
	pozicija_stranke = Pozicija.objects.filter(organizacija__stranka__gt=0)
	claniodborov = ClanOdbora.objects.all().order_by("od", "do", "poslanec__oseba__id")
	pozicija_odbori = Pozicija.objects.filter(organizacija__delovnotelo__gt=0)
	
	def check_from_to_dates(s, d, sfx):
		if d.od != s.od:
			errors.append("- napačen začetni datum (%s vs. %s): %s" % (s.od, d.od, sfx))
		if d.do != s.do:
			errors.append("- napačen končni datum (%s vs. %s): %s" % (s.do, d.do, sfx))
	
	def check_old_new_data(qs, filters, sfxer):
		for item in qs:
			sfx = sfxer(item)
			ps = Pozicija.objects.filter(**filters(item))
			psc = ps.count()
			if not psc:
				errors.append("- ne obstaja: %s" % sfx)
			elif psc == 1:
				check_from_to_dates(item, ps[0], sfx)
			else: # več kot 1 pozicija, omejitev glede na en datum in drugi datum
				try:
					p = ps.get(od=item.od, do=item.do)
				except MultipleObjectsReturned:
					errors.append("- več Pozicij z istim začetnim in končnim datumom (%s - %s): %s" % (item.od, item.do, sfx))
				except ObjectDoesNotExist:
					try:
						p = ps.get(od=item.od)
						check_from_to_dates(item, p, sfx)
					except MultipleObjectsReturned:
						errors.append("- več Pozicij z istim začetnim datumom (%s): %s" % (item.od, sfx))
					except ObjectDoesNotExist:
						errors.append("- ni Pozicije s tem začetnim datumom (%s): %s" % (item.od, sfx))
					try:
						p = ps.get(do=item.do)
						check_from_to_dates(item, p, sfx)
					except MultipleObjectsReturned:
						errors.append("- več Pozicij z istim končnim datumom (%s): %s" % (item.do, sfx))
					except ObjectDoesNotExist:
						errors.append("- ni Pozicije z tem končnim datumom (%s): %s" % (item.do, sfx))
	
	fc = funkcije.count()
	pfc = pozicija_dz.count()
	if pfc != fc:
		errors.append("Različno število Funkcij (%d) in Pozicij v državnem zboru (%d)" % (fc, pfc))
	
	if VERBOSE:
		check_old_new_data(
			funkcije,
			lambda i: {
				'organizacija__drzavnizbor__mandat__id':  i.mandat_id,
				'oseba__id': i.oseba_id
			},
			lambda i: "Pozicija za Funkcijo v Mandatu %s za Osebo %s (%d)" % (i.mandat, i.oseba, i.oseba_id)
		)
	
	csce = clanistranke.filter(stranka__gt=0).count()
	pcsc = pozicija_stranke.count()
	if csce != pcsc:
		errors.append("Različno število ClanStranke s stranko (%d) in Pozicij v strankah (%d)" % (csce, pcsc))
	
	if VERBOSE:
		check_old_new_data(
			clanistranke.filter(stranka__gt=0),
			lambda i: {
				'organizacija__stranka__id':  i.stranka_id,
				'oseba__id': i.oseba_id
			},
			lambda i: "Pozicija za ClanStranke v Stranki %s za Osebo %s (%d)" % (i.stranka, i.oseba, i.oseba_id)
		)
	
	coc = claniodborov.count()
	pcoc = pozicija_odbori.count()
	if coc != pcoc:
		errors.append("Različno število ClanOdbora (%d) in Pozicij v delovnih telesih (%d)" % (coc, pcoc))
	
	if VERBOSE:
		check_old_new_data(
			claniodborov,
			lambda i: {
				'organizacija__delovnotelo__id':  i.odbor_id,
				'oseba__id': i.poslanec.oseba_id
			},
			lambda i: "Pozicija za ClanOdbora v DelovnemTelesu %s za Osebo %s (%d)" % (i.odbor, i.poslanec.oseba, i.poslanec.oseba_id)
		)
	
	return errors
	

@login_required
def data_check(request):
	global VERBOSE
	if request.GET.has_key("verbose"):
		VERBOSE = True
	
	t1 = time.time()
	
	mandat_errors = _check_mandat()
	oseba_errors = _check_oseba()
	funkcija_errors = _check_funkcija()
	delovnotelo_errors = _check_delovnotelo()
	seja_errors = _check_seja()
	zasedanje_errors = _check_zasedanje()
	zapis_errors = _check_zapis()
	glasovanje_errors = _check_glasovanje()
	glas_errors = _check_glas()
	#clanstranke_errors = _check_clanstranke()
	clanstranke_errors = []
	
	#translation_errors = _check_translation()
	
	t2 = time.time()
	
	context = {
		'mandat_errors': mandat_errors,
		'oseba_errors': oseba_errors,
		'funkcija_errors': funkcija_errors,
		'delovnotelo_errors': delovnotelo_errors,
		'seja_errors': seja_errors,
		'zasedanje_errors': zasedanje_errors,
		'zapis_errors': zapis_errors,
		'glasovanje_errors': glasovanje_errors,
		'glas_errors': glas_errors,
		'clanstranke_errors': clanstranke_errors,
		#'translation_errors': translation_errors,
		'took': t2-t1,
	}
	return render(request, "data_check.html", context)
