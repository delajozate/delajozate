# Sets search index models for haystack
import haystack
from haystack.fields import CharField
from haystack.sites import site
from search.models import Zapis

class ZasedanjaIndex(haystack.indexes.SearchIndex):
    ime_seje = CharField(model_attr='zasedanje__seja__naslov')
    ime_zasedanja = CharField(model_attr='zasedanje__naslov')
    datum = CharField(model_attr='zasedanje__datum')
    govorec = CharField(model_attr='govorec', null=True)
    text = CharField(document=True, use_template=True, template_name='search/indexes/zasedanja.txt')

site.register(Zapis, ZasedanjaIndex)
    