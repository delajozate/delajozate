import datetime
from haystack import indexes
from haystack import site
from magnetogrami.models import Seja, Zapis


class ZapisIndex(indexes.SearchIndex):
	text = indexes.CharField(document=True, use_template=True)
	author_t = indexes.CharField(model_attr='govorec_oseba', null=True)
	pub_date_dt = indexes.DateTimeField(model_attr='datum')
	
	def get_model(self):
		return Zapis
	
	def index_queryset(self):
		return self.get_model().objects.all().order_by('zasedanje__datum', 'seq')

site.register(Zapis, ZapisIndex)
