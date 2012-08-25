import re

from django.views.decorators.cache import cache_page
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.db.models import Q

from delajozate.dz.models import DelovnoTelo
from delajozate.magnetogrami.models import Seja, Zasedanje, Zapis

def tipi_sej(request):
    context = {
        'object_list': DelovnoTelo.objects.exclude(dz_id=None).order_by('-od', '-do'), # XXX FIXME
        }
    
    return render_to_response('magnetogrami/tipi_sej.html', RequestContext(request, context))

def seja_list(request, mdt, mandat=None):
    
    delovno_telo = None
    zasedanja = Zasedanje.objects.filter(seja__delovno_telo=mdt).filter(Q(tip='magnetogram') |Q(tip='dobesednizapis')).select_related('seja').order_by('-datum')
    
    if mandat is not None:
        zasedanja.filter(seja__mandat=mandat)
        if mdt != 'dz': # XXX FIXME add DelovnoTelo?
            delovno_telo = DelovnoTelo.objects.get(dz_id=mdt, mandat__st=mandat)

    context = {
        'object_list': zasedanja,
        'delovno_telo': delovno_telo,
        }
    return render_to_response('magnetogrami/seja_list.html', RequestContext(request, context))


def _get_seja_zapisi(request, mdt, mandat, slug, datum_zasedanja=None):
    #assert mdt == 'dz' # for now
    seja = Seja.objects.get(mandat=mandat, slug=slug, delovno_telo=mdt)

    if datum_zasedanja is None:
        try:
            zasedanje = Zasedanje.objects.filter(
                Q(seja=seja, tip='dobesednizapis') |
                Q(seja=seja, tip='magnetogram')).order_by('datum')[0]
        except IndexError:
            zasedanje = None
            zapisi = []
    else:
        zasedanje = Zasedanje.objects.filter(seja=seja, datum=datum_zasedanja).filter(Q(tip='dobesednizapis') | Q(tip='magnetogram')).select_related('zapis')

    if zasedanje is not None:
        zapisi = Zapis.objects.filter(zasedanje=zasedanje).select_related('govorec_oseba', 'zasedanje')

    #add stranka/stranke to govorec_oseba
    for zapis in zapisi:
        if zapis.govorec_oseba:
            zapis.govorec_oseba.stranke = zapis.govorec_oseba.clanstranke_set.filter(od__lte=datum_zasedanja, do__gte=datum_zasedanja)

    return seja, zasedanje, zapisi


def seja(request, mdt, mandat, slug, datum_zasedanja=None):
    seja, zasedanje, zapisi = _get_seja_zapisi(request, mdt, mandat, slug, datum_zasedanja)

    context = {
        'seja': seja,
        'zasedanje': zasedanje,
        'zapisi': zapisi,
        }
    return render_to_response("magnetogrami/seja.html", RequestContext(request, context))


def citat(request, mdt, mandat, slug, datum_zasedanja, odstavek):
    seja, zasedanje, zapisi = _get_seja_zapisi(request, mdt, mandat, slug, datum_zasedanja)

    odstavek = int(odstavek)
    zapisi = [zapisi.get(seq=odstavek)]

    context = {
        'seja': seja,
        'zasedanje': zasedanje,
        'zapisi': zapisi,
        'citirano': odstavek,
        }
    return render_to_response("magnetogrami/citat.html", RequestContext(request, context))





