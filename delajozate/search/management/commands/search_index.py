from django.core.management.base import BaseCommand, CommandError
from search.importer import Importer

class Command(BaseCommand):
    args = "data_path"
    help = "Imports data into solr index"
    def handle(self, *args, **options):
        from delajozate.search.simple import search_register
        
        for model, searchmodel in search_register.items():
            print 'Indexing', model.__name__
            searchmodel.index()
