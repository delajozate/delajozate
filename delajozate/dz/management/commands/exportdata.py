from django.core.management.base import NoArgsCommand
from delajozate.dz.export import exportdata

class Command(NoArgsCommand):
    help = "Create a data export into fixtures/exported_data.json"
    
    def handle_noargs(self, **options):
        exportdata(indent=4)
    
