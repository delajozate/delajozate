from django.core.management.base import BaseCommand, CommandError
from search.importer import Importer
from optparse import make_option

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--full',
            action='store_true',
            dest='full',
            default=False,
            help='Make a full re-index'),
        )

    args = "data_path"
    help = "Imports data into solr index"
    def handle(self, *args, **options):
        from delajozate.search.simple import search_register
        for model, searchmodel in search_register.items():
            print 'Indexing', model.__name__
            if hasattr(searchmodel, 'full_index') and options.get('full'):
                searchmodel().full_index()
            else:
                searchmodel().index()
