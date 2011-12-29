from django.core.management.base import BaseCommand
from iskanje.importer import Importer

class Command(BaseCommand):
    help = "Imports data into solr index"
    def handle(self, *args, **options):
        importer = Importer()
        importer.do_solr_import()
