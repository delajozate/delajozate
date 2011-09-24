# Sets search index models for haystack
from haystack.indexes import CharField, SearchIndex
from haystack import site
from search.models import Povezava

class MagnetogramIndex(SearchIndex):
    text = CharField(document=True, use_template=False)

site.register(Povezava, MagnetogramIndex)