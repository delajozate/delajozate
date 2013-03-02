from django.conf import settings
from django.shortcuts import render
from dz.models import Oseba
from magnetogrami.models import Seja, Zapis
import pysolarized


def index(request):
	context = { "osebe": [], "stranke": [], "zapisi": [] }
	if request.GET.has_key('q'):
		# Do search
		solr = pysolarized.Solr(settings.SOLR_URL)
		results = solr.query(request.GET.get('q'), sort=["tip asc", "datum_zapisa desc", "datum_od desc"])

		if not results or results.results_count == 0:
			context["results"] = None
		else:
			for result in results.documents:
				if result["tip"] == "oseba":
					context["osebe"].append({"ime": result["ime"], "slug": result["str_slug"]})
				elif result["tip"] == "stranka":
					stranka = {"ime" : result["ime"],
					            "okrajsava": result["str_okrajsava"] }

					if "datum_od" in result:
						stranka["od"] = pysolarized.from_solr_date(result["datum_od"])
					if "datum_do" in result:
						stranka["do"] = pysolarized.from_solr_date(result["datum_do"])

					context["stranke"].append(stranka)
				elif result["tip"] == "zapis":
					id = result["id"]
					date = pysolarized.from_solr_date(result["datum_zapisa"])
					zapis = {"ime_seje": result["str_ime_seje"],
					         "datum": date,
					         "permalink": result["str_permalink"],
					         "seq": result["str_seq"], }

					if "id_oseba" in result:
						zapis["ime_govorca"] = result["txt_govorec"]
						zapis["govorec_slug"] = result["str_govorec_slug"]

					if id in results.highlights:
						zapis["vsebina"] = results.highlights[id].get("vsebina", None)
					elif "vsebina" in result:
						zapis["vsebina"] = result["vsebina"]

					context["zapisi"].append(zapis)

		context["results"] = results.documents

	return render(request, 'search.html', context)