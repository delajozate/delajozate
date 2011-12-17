
import re

from django.views.decorators.cache import cache_page
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.db.models import Q

from delajozate.magnetogrami.models import Seja, SejaInfo, Zasedanje, Zapis

def seja_list(request):
	zasedanja = Zasedanje.objects.filter(Q(tip='magnetogram') | Q(tip='dobesednizapis')).select_related('seja').order_by('-datum')
	
	context = {
		'object_list': zasedanja,
		}
	return render_to_response('magnetogrami/seja_list.html', RequestContext(request, context))

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
			zapisi = []
	else:
		zasedanje = Zasedanje.objects.filter(seja=seja, datum=datum_zasedanja).filter(Q(tip='dobesednizapis')|Q(tip='magnetogram')).select_related('zapis')
	
	if zasedanje is not None:
		zapisi = Zapis.objects.filter(zasedanje=zasedanje).select_related('govorec_oseba')
	
	context = {
		'seja': seja,
		'zasedanje': zasedanje,
		'zapisi': zapisi,
		}
	return render_to_response("magnetogrami/seja.html", RequestContext(request, context))
