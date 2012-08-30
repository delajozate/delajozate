import datetime
from haystack import indexes
from haystack import site
from magnetogrami.models import Seja, Zapis


class ZapisIndex(indexes.SearchIndex):
	text = indexes.CharField(document=True, use_template=True)
	govorec_t = indexes.CharField(model_attr='govorec_oseba', null=True)
	govorec_slug_t = indexes.CharField(model_attr='govorec_slug', null=True)
	ime_seje_t = indexes.CharField(model_attr='ime_seje', null=True)
	permalink_t = indexes.CharField(model_attr='permalink', null=True)
	seq_i = indexes.IntegerField(model_attr='seq')
	pub_date_dt = indexes.DateTimeField(model_attr='datum')
	
	def get_model(self):
		return Zapis
	
	def index_queryset(self):
		return self.get_model().objects.all().order_by('zasedanje__datum', 'seq').select_related('zasedanje', 'govorec_oseba', 'zasedanje__seja')
	

site.register(Zapis, ZapisIndex)
