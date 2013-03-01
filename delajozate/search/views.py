from django.conf import settings
from django.shortcuts import render
from dz.models import Oseba
from magnetogrami.models import Seja, Zapis
import pysolarized


def index(request):
	context = {}
	if request.GET.has_key('q'):
		# Do search
		solr = pysolarized.Solr(settings.SOLR_URL)
		results = solr.query(request.GET.get('q'))

		context["osebe"] = []
		context["zapisi"] = []

		for result in results.documents:
			# TODO: add info fetched from DB to solr index
			if result["tip"] == "oseba":
				oseba = Oseba.objects.get(pk=int(result["id_db"]))
				context["osebe"].append({"ime": result["ime"], "slug": oseba.slug})
			elif result["tip"] == "zapis":
				id = result["id"]
				seja = Seja.objects.get(pk=int(result["id_seja"]))
				zapis_db = Zapis.objects.get(pk=int(result["id_db"]))
				date = pysolarized.from_solr_date(result["datum_zapisa"])
				zapis = {"ime_seje": seja.naslov,
				         "datum": date,
				         "permalink": zapis_db.permalink,
				         "seq": zapis_db.seq, }

				if "id_oseba" in result:
					govorec = Oseba.objects.get(pk=int(result["id_oseba"]))
					zapis["ime_govorca"] = "%s %s" % (govorec.ime, govorec.priimek,)
					zapis["govorec_slug"] = govorec.slug

				if id in results.highlights:
					zapis["vsebina"] = results.highlights[id].get("vsebina", None)

				context["zapisi"].append(zapis)

		context["results"] = results.documents
		print context

	return render(request, 'search.html', context)