
from django.core.management.base import BaseCommand
from django.utils import simplejson

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
    )
    args = ""
    help = "potegne dogodke v DZRS iz hrcka"

    def handle(self, *args, **options):
        from delajozate.cal.models import fetch_dzrs_events
        fetch_dzrs_events()