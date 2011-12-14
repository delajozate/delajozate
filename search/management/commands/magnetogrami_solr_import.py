from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from search.importer import Importer

class Command(BaseCommand):
    args = "data_path"
    help = "Imports data into solr index"
    def handle(self, *args, **options):
        try:
            data_path = args[0]
        except IndexError:
            raise CommandError("Invalid parameters given: missing data path.")
        importer = Importer(data_path)
        importer.do_import()
