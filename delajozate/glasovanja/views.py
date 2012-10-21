# Create your views here.

from django.shortcuts import render
from magnetogrami.models import Glasovanje, Glas

def index(request):
    context = {
        'object_list': Glasovanje.objects.all(),
        }
    return render(request, 'glasovanja.html', context)

def glasovanje(request, datum, id):
    glasovi = Glas.objects.filter(glasovanje__id=id).select_related('oseba')
    context = {
        'objects': glasovi
    }
    return render(request, 'glasovanje.html', context)