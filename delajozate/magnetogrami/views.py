import re

from django.views.decorators.cache import cache_page
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db.models import Q

from delajozate.dz.models import DelovnoTelo
from delajozate.magnetogrami.models import Seja, Zasedanje, Zapis

def tipi_sej(request):
    context = {
        'object_list': DelovnoTelo.objects.exclude(dz_id=None).order_by('-od', '-do').select_related('mandat'), # XXX FIXME
        }
    
    return render(request, 'magnetogrami/tipi_sej.html', context)

def seja_list(request, mdt=None, mandat=None):
    
    delovno_telo = None
    zasedanja = Zasedanje.objects.filter(Q(tip='magnetogram') |Q(tip='dobesednizapis')).select_related('seja').order_by('-datum')

    if mdt is not None:
        zasedanja = zasedanja.filter(seja__delovno_telo=mdt)
        if mdt != 'dz': # XXX FIXME add DelovnoTelo?
            delovno_telo = DelovnoTelo.objects.get(dz_id=mdt, mandat__st=mandat)

    if mandat is not None:
        zasedanja.filter(seja__mandat=mandat)
    
    context = {
        'object_list': zasedanja,
        'delovno_telo': delovno_telo,
        }
    return render(request, 'magnetogrami/seja_list.html', context)


def _get_seja_zapisi(request, mdt, mandat, slug, datum_zasedanja=None):
    #assert mdt == 'dz' # for now
    seja = get_object_or_404(Seja, mandat=mandat, slug=slug, delovno_telo=mdt)

    if datum_zasedanja is None:
        try:
            zasedanje = Zasedanje.objects.filter(
                Q(seja=seja, tip='dobesednizapis') |
                Q(seja=seja, tip='magnetogram')).select_related('zapis').order_by('datum')[0]
        except IndexError:
            zasedanje = None
            zapisi = []
    else:
        zasedanje = Zasedanje.objects.filter(seja=seja, datum=datum_zasedanja).filter(Q(tip='dobesednizapis') | Q(tip='magnetogram')).select_related('zapis')[0]

    if zasedanje is not None:
        zapisi = Zapis.objects.filter(zasedanje=zasedanje).select_related('govorec_oseba', 'zasedanje', 'zasedanje__seja')

    return seja, zasedanje, zapisi


def seja(request, mdt, mandat, slug, datum_zasedanja=None):
    if slug.startswith('0'):
        newslug = re.sub('^0*', '', slug)
        return HttpResponseRedirect(reverse('delajozate.magnetogrami.views.seja', args=(mandat, mdt, newslug, datum_zasedanja)))

    seja, zasedanje, zapisi = _get_seja_zapisi(request, mdt, mandat, slug, datum_zasedanja)

    context = {
        'seja': seja,
        'zasedanje': zasedanje,
        'zapisi': zapisi,
        }
    return render(request, "magnetogrami/seja.html", context)


def citat(request, mdt, mandat, slug, datum_zasedanja, odstavek):
    if slug.startswith('0'):
        newslug = re.sub('^0*', '', slug)
        return HttpResponseRedirect(reverse('delajozate.magnetogrami.views.citat', args=(mandat, mdt, newslug, datum_zasedanja, odstavek)))

    seja, zasedanje, zapisi = _get_seja_zapisi(request, mdt, mandat, slug, datum_zasedanja)

    odstavek = int(odstavek)
    zapisi = [zapisi.get(seq=odstavek)]

    context = {
        'seja': seja,
        'zasedanje': zasedanje,
        'zapisi': zapisi,
        'citirano': odstavek,
        }
    return render(request, "magnetogrami/citat.html", context)





