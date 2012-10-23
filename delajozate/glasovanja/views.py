# Create your views here.

import datetime

from django.shortcuts import render
from django.http import Http404

from magnetogrami.models import Glasovanje, Glas

def index(request):
    context = {
        'object_list': Glasovanje.objects.all(),
        }
    return render(request, 'glasovanja.html', context)

def glasovanje(request, datum, ura=None, pk=None):
    datum = datetime.datetime.strptime(datum, '%Y-%m-%d').date()
    
    if ura is not None:
        ura = datetime.datetime.strptime(ura, '%H:%M:%S').time()
        glasovi = Glas.objects.filter(
            glasovanje__datum=datum,
            glasovanje__ura=ura).select_related('oseba')
        
    elif pk is not None:
        glasovi.filter(glasovanje__id=pk).select_related('oseba')
    else:
        raise Http404
    
    context = {
        'objects': glasovi
    }
    return render(request, 'glasovanje.html', context)