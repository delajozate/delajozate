# Create your views here.
from django.http import HttpResponse
from search.importer import Importer

def do_import(request):
    importer = Importer("/home/jernej/Projekti/Opendata-hackday-2011/data/")
    importer.do_import()
    return HttpResponse("Importing...")