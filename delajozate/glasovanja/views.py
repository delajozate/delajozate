# Create your views here.

import datetime
import json

from django.shortcuts import render
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from magnetogrami.models import Glasovanje, Glas, Seja, Zasedanje

def index(request):
    glasovanja_list = Glasovanje.objects.all().select_related('seja')
    paginator = Paginator(glasovanja_list, 100)
    page = request.GET.get('page', 1)
    try:
        glasovanja = paginator.page(page)
    except PageNotAnInteger:
        glasovanja = paginator.page(1)
    except EmptyPage:
        glasovanja = paginator.page(paginator.num_pages)
    
    context = {
        'glasovanja': glasovanja,
        }
    return render(request, 'glasovanja.html', context)

def glasovanje(request, datum, ura=None, pk=None):
    datum = datetime.datetime.strptime(datum, '%Y-%m-%d').date()
    
    if ura is not None:
        ura = datetime.datetime.strptime(ura, '%H:%M:%S').time()
        glasovi = Glas.objects.filter(
            glasovanje__datum=datum,
            glasovanje__ura=ura)
    elif pk is not None:
        glasovi = Glas.objects.filter(glasovanje__id=pk)
    else:
        raise Http404
    
    glasovi = glasovi.select_related('glasovanje', 'glasovanje__seja')
    seja = glasovi[0].glasovanje.seja
    zasedanja = Zasedanje.objects.filter(seja=seja, datum=datum).order_by('-id')
    
    glasovi = glasovi.select_related('oseba')
    context = {
        'objects': glasovi,
        'seja': seja,
        'zasedanja': zasedanja,
    }
    return render(request, 'glasovanje.html', context)