# coding: utf-8
import datetime
import time
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.db import connection
from django.contrib.auth.decorators import login_required

from dz.models import Mandat, Oseba, Funkcija, DelovnoTelo
from magnetogrami.models import Glasovanje, Glas, Zapis

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
    
    sql = """SELECT Count(*) from (SELECT Q.datum, Q.st_poslancev, Q.st_poslancev > 90 as prevec_poslancev from (SELECT D.datum, (select count(*) from dz_funkcija F where F.funkcija='poslanec' AND F.od <= D.datum AND F.do > D.datum) as st_poslancev  from (select '1992-12-23'::date + s.t as datum from generate_series(0,(date_trunc('day', now())::date - '1992-12-23'::date)) as s(t)) AS D) AS Q where Q.st_poslancev > 90) as QQ;"""
    cur.execute(sql, [])
    data = cur.fetchall()
    if data:
        funkcija_errors.append(u'Število dni, ko je več kot 90 poslancev: %s' % (data[0]))
    
    
    
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

@login_required
def data_check(request):
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
        'took': t2-t1,
    }
    return render(request, "data_check.html", context)
