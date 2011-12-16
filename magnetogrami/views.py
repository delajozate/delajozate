
import re

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.db.models import Q

from delajozate.magnetogrami.models import Seja, SejaInfo, Zasedanje, Zapis

def seja(request, mdt, mandat, slug, datum_zasedanja=None):
    assert mdt == 'dz' # for now
    seja = Seja.objects.get(mandat=mandat, slug=slug)
    
    if datum_zasedanja is None:
        try:
            zasedanje = Zasedanje.objects.filter(
                Q(seja=seja, tip='dobesednizapis') | 
                Q(seja=seja, tip='magnetogram')).order_by('datum')[0]
        except IndexError:
            zasedanje = None
    else:
        zasedanje = Zasedanje.objects.filter(seja=seja, datum=datum_zasedanja).get(Q(tip='dobesednizapis')|Q(tip='magnetogram'))
    
    context = {
        'seja': seja,
        'zasedanje': zasedanje,
        }
    return render_to_response("magnetogrami/seja.html", RequestContext(request, context))
