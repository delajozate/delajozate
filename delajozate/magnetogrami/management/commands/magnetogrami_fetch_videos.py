
from django.core.management.base import BaseCommand
from django.utils import simplejson

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
    )
    args = ""
    help = "poscrapa linke z RTV Slo"

    def handle(self, *args, **options):
        from delajozate.magnetogrami.scrapers import run_videos
        run_videos()