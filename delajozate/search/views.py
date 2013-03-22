from django.conf import settings
from django.shortcuts import render
from dz.models import Oseba
from magnetogrami.models import Seja, Zapis
import pysolarized
from delajozate.search.simple import search_register_by_name

RESULTS_PAGE_SIZE = 30

def index(request):
	
	context = {
		'tipi': [{'value': k,'name': v._meta.verbose_name_plural} for k,v in search_register_by_name.iteritems()]
		}

	if request.GET.has_key('q'):
		context["query"] = query = request.GET["q"]
		context['qfilter'] = qfilter = request.GET.getlist('tip')
		filterquery = None
		if qfilter:
			qfilter = [i for i in qfilter if i in search_register_by_name]
			filterquery = {'tip': '(%s)' % (' OR '.join(qfilter),)}
		# Check for current page
		page = 1        # We start counting from 1 otherwise page = 0 confuses template ifs
		if request.GET.has_key("page"):
			try:
				page = max(1, int(request.GET["page"]))
			except ValueError:
				page = 1

		# Do search
		solr = pysolarized.Solr(settings.SOLR_URL)
		
		results = solr.query(query,
		                     sort=["score desc"],
		                     filters=filterquery,
		                     start=(page - 1) * RESULTS_PAGE_SIZE,
		                     rows=RESULTS_PAGE_SIZE)

		# Parse search results
		if not results or results.results_count == 0:
			context["results"] = None
		else:
			context['results'] = results.documents
			# Figure out pagination
			if results.results_count > RESULTS_PAGE_SIZE:
				if results.start_index > 0:
					context["prev_page"] = max(1, page - 1)
				# Page + 1 since we're counting from 0
				if page * RESULTS_PAGE_SIZE < results.results_count:
					context["next_page"] = page + 1

		context["results"] = results.documents
		context['highlights'] = results.highlights
		
	return render(request, 'search.html', context)
