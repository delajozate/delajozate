import json
import os
import re
import time
from django.conf import settings
from dz.models import Oseba, Stranka
import pysolarized

import dateutil.parser
from django.db import transaction, connection
from magnetogrami.models import Seja, Zasedanje, Zapis
from temporal import END_OF_TIME


class Importer():
	def parse_time(self, time_string):
		try:
			parsed_time = time.strptime(time_string, "%H.%S")
		except:
			try:
				parsed_time = time.strptime(time_string, "%H")
			except:
				parsed_time = None

		if parsed_time:
			return time.strftime("%H:%S", parsed_time)
		else:
			return None

	def do_database_import(self, file_directory):
		files = os.listdir(file_directory)
		Seja.objects.all().delete()
		Zasedanje.objects.all().delete()
		Zapis.objects.all().delete()
		govorci_fn = os.path.join(os.path.dirname(__file__), 'govorci.json')
		govorci_map = json.load(open(govorci_fn))

		for file in sorted(files):
			print file, "..."
			counter = 0
			for fileData in open(os.path.join(file_directory, file), 'r'):
				counter = counter + 1
				print counter, ".."
				# Parse JSON data and create models
				jsonData = json.loads(fileData.replace("\\\\", "\\"))
				with transaction.commit_on_success():
					seja = Seja()
					seja.mandat = int(jsonData.get('mandat'))
					naslov_seje = jsonData.get('naslov')
					if naslov_seje.startswith('0.  seja'):
						continue # foo data
					seja.naslov = naslov_seje
					match = re.search('(\d+)\.\s*(redna|izredna)', naslov_seje, re.I)
					if not match:
						print naslov_seje
					seja_slug = ('%s-%s' % match.groups()).lower()
					seja.slug = seja_slug
					try:
						seja.datum_zacetka = dateutil.parser.parse(jsonData.get('datum_zacetka'), dayfirst=True)
					except:
						seja.datum_zacetka = None
					seja.seja = jsonData.get('seja')
					seja.url = jsonData.get('url')
					seja.save()

					# jsonSeja objects
					for jsonSeja in jsonData.get('seja_info'):
						sejaInfo = SejaInfo()
						sejaInfo.seja = seja
						sejaInfo.url = jsonSeja.get('url')
						sejaInfo.naslov = jsonSeja.get('naslov')
						sejaInfo.datum = dateutil.parser.parse(jsonSeja.get('datum'), dayfirst=True)
						sejaInfo.save()

					# Zasedanja
					for jsonZasedanje in jsonData.get('zasedanja'):
						for jsonPovezava in jsonZasedanje.get('povezave'):
							zasedanje = Zasedanje()
							zasedanje.datum = dateutil.parser.parse(jsonZasedanje.get('datum'), dayfirst=True)
							zasedanje.seja = seja

							if jsonPovezava.get('zacetek'):
								zasedanje.zacetek = self.parse_time(jsonPovezava.get('zacetek'))
							if jsonPovezava.get('konec'):
								zasedanje.konec = self.parse_time(jsonPovezava.get('konec'))

							zasedanje.tip = jsonPovezava.get('tip')
							zasedanje.naslov = jsonPovezava.get('naslov')
							zasedanje.save()

							cursor = connection.cursor()
							count = 0
							keys = ['seq', 'zasedanje_id', 'govorec', 'govorec_oseba_id', 'odstavki']

							values = []
							for jsonOdsek in jsonPovezava.get('odseki'):
								for jsonZapis in jsonOdsek.get('zapisi'):
									govorec = jsonZapis.get('govorec')
									if govorec is not None:
										govorec = govorec.strip()
									oseba_id = govorci_map.get(govorec, None)
									for ods in jsonZapis.get('odstavki'):
										values.extend([
											count,
											zasedanje.id,
											govorec,
											oseba_id,
											ods,
										])
										count += 1

							params = values
							onerowtempl = '(' + ', '.join(['%s'] * len(keys)) + ')'
							all_rows_template = ', '.join([onerowtempl] * (len(params) / len(keys)))
							sql = '''INSERT INTO %s (%s) VALUES %s''' % (
								Zapis._meta.db_table,
								', '.join(keys),
								all_rows_template)
							if params:
								cursor.execute(sql, params)
					if seja.datum_zacetka is None:
						# use as an alternative
						try:
							seja.datum_zacetka = Zasedanje.objects.filter(seja=seja).order_by('-datum')[0].datum
						except:
							pass
					seja.save()

	def do_solr_import(self):
		solr = pysolarized.Solr(settings.SOLR_URL)
		solr.deleteAll()
		for oseba in Oseba.objects.all():
			doc = { "id": "os_%s" % (oseba.id,), "id_db": oseba.id, "tip": "oseba",
					"ime": "%s %s" % (oseba.ime, oseba.priimek,) }

			if oseba.twitter:
				doc["str_twitter"] = oseba.twitter

			if oseba.facebook:
				doc["str_facebook"] = oseba.facebook

			if oseba.rojstni_dan:
				doc["datum_rojstva"] = pysolarized.to_solr_date(oseba.rojstni_dan)

			solr.add(doc)

		for stranka in Stranka.objects.all():
			doc = { "id": "st_%s" % (stranka.id,), "id_db": stranka.id, "tip": "stranka",
					"ime": stranka.ime, "str_okrajsava": stranka.okrajsava}

			if stranka.od:
				doc["datum_od"] = pysolarized.to_solr_date(stranka.od)

			if stranka.do != END_OF_TIME:
				doc["datum_do"] = pysolarized.to_solr_date(stranka.do)

			solr.add(doc)

		for seja in Seja.objects.all():
			for zasedanje in seja.zasedanje_set.all():
				doc = { "id": "zas_%s" % (zasedanje.id, ), "id_db": zasedanje.id, "tip": "zasedanje" }
				if zasedanje.naslov:
					doc["ime"] = zasedanje.naslov
				if zasedanje.datum:
					doc["datum_zasedanja"] = pysolarized.to_solr_date(zasedanje.datum)
				if zasedanje.tip:
					doc["str_tip"] = zasedanje.tip

				zasedanje_txt = []
				for zapis in zasedanje.zapis_set.all():
					zapis_doc = { "id": "zap_%s" % (zapis.id, ), "id_db": zapis.id, "tip": "zapis",
								"vsebina": zapis.odstavki}

					if zapis.govorec:
						zapis_doc["id_oseba"] = zapis.govorec_oseba_id
						if zapis.govorec_oseba:
							zapis_doc["txt_govorec"] = "%s %s" % (zapis.govorec_oseba.ime, zapis.govorec_oseba.priimek,)

					zapis_doc["id_zasedanje"] = zapis.zasedanje_id
					zapis_doc["id_seja"] = zapis.zasedanje.seja_id

					if zapis.datum:
						zapis_doc["datum_zapisa"] = pysolarized.to_solr_date(zapis.datum)

					solr.add(zapis_doc)
					zasedanje_txt.append(zapis.odstavki)

				doc["vsa_polja"] = zasedanje_txt
				solr.add(doc)
				solr.commit()

