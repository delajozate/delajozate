from collections import defaultdict
from django.core.management.base import NoArgsCommand
from dz.models import Stranka, Oseba
from dz.templatetags.dz_extras import datum_filter
from magnetogrami.models import Glasovanje

class Command(NoArgsCommand):

	def handle_noargs(self, **options):

		glasovi = defaultdict(dict)
		for glasovanje in Glasovanje.objects.select_related().all():
			if glasovanje.datum is None:
				continue

			glasovanje_strank = {}
			for glas in glasovanje.glas_set.select_related().all():
				clanstvo = datum_filter(glas.oseba.clanstvo(), glasovanje.datum)
				if len(clanstvo) == 0:
					continue

				stranka_id = clanstvo[0].stranka_id

				if stranka_id not in glasovanje_strank:
					glasovanje_strank[stranka_id] = defaultdict(list)

				if glas.glasoval == "Za":
					glasovanje_strank[stranka_id]["Za"].append(glas.oseba_id)
				elif glas.glasoval == "Proti":
					glasovanje_strank[stranka_id]["Proti"].append(glas.oseba_id)

			for stranka, vrednost in glasovanje_strank.items():
				if stranka not in glasovi:
					glasovi[stranka] = []

				glasovi[stranka].append( { "Za" : vrednost["Za"], "Proti": vrednost["Proti"] })

		for stranka, glasovanja in glasovi.items():
			tocke = defaultdict(int)

			try:
				stranka = Stranka.objects.get(pk=stranka).ime
			except Stranka.DoesNotExist:
				stranka = "Neznano"

			print " == ", stranka, " == "
			for glasovanje in glasovanja:

				if len(glasovanje["Za"]) > len(glasovanje["Proti"]):
					minority = glasovanje["Proti"]
				else:
					minority = glasovanje["Za"]

				for glasovalec in minority:
					tocke[glasovalec] += 1

			o_list = [(pts, oseba_id) for oseba_id, pts in tocke.items()]

			for pts, oseba_id in sorted(o_list):
				oseba = Oseba.objects.get(pk=oseba_id)
				print oseba.ime, oseba.priimek, pts
