from django.core.management.base import BaseCommand
from search.importer import Importer

class Command(BaseCommand):
    args = ""
    help = "Imports data into solr index"

    def handle(self, *args, **options):
        importer = Importer("/home/jernej/dzrs/")
        importer.do_import()