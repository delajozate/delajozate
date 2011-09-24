# Create your views here.
from django.http import HttpResponse

def do_import(request):
    return HttpResponse("Importing...")