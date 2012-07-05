
from django.core.management.base import BaseCommand
from django.utils import simplejson

class Command(BaseCommand):
	option_list = BaseCommand.option_list + (
	)
	args = ""
	help = "nalozi seje"

	def handle(self, *args, **options):
		import urllib
		from pprint import pprint
		from delajozate.magnetogrami.models import seja_import_one
		
		
		def get_last_id():
			try:
				return int(open('seja_id.txt').read())
			except:
				return 0
		set_last_id = lambda x: open('seja_id.txt','w').write(str(x))
		
		
		last_id = get_last_id()
		url_template = 'http://localhost:8000/drzava/dzrs/seja/?valid_end=9999-12-31&id__gte=%d'
		
		req = urllib.urlopen(url_template % last_id)
		data = req.read()
		
		if req.getcode() != 200:
			raise ValueError("Something wrong with response!")
		
		
		j = simplejson.loads(data)
		ids = []
		for item in j:
			print item['id'], item['naslov']
			seja_import_one(item['json'])
			ids.append(item['id'])
		
		print max(ids)
		set_last_id(max(ids))