from django.core.management.base import BaseCommand, CommandError
from iskanje.importer import Importer

class Command(BaseCommand):
    args = "data_path"
    help = "Imports data into solr index"
    def handle(self, *args, **options):
        try:
            data_path = args[0]
        except IndexError:
            raise CommandError("Invalid parameters given: missing data path.")
        importer = Importer()
        importer.do_database_import(data_path)
