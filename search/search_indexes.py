# Sets search index models for haystack
import haystack
from haystack.fields import CharField, DateField, IntegerField
from haystack.sites import site
from search.models import Zapis, Seja

# Glavna uporaba je za iskanje sej, kjer se je celotna seja vrtela okoli iskane tematike
# (Besedilo ni razdrobljeno)
class SejeIndex(haystack.indexes.SearchIndex):
    ime_seje = CharField(model_attr='naslov')
    mandat = IntegerField(model_attr='mandat')
    text = CharField(document=True, use_template=True, template_name='search/indexes/seje.txt')

# Uporabno za iskanje dolocenih izjav, za natancnejse filtriranje se da implementirat drill-down
class ZasedanjaIndex(haystack.indexes.SearchIndex):
    ime_seje = CharField(model_attr='zasedanje__seja__naslov', faceted=True)
    ime_zasedanja = CharField(model_attr='zasedanje__naslov', faceted=True)
    govorec = CharField(model_attr='govorec', null=True, faceted=True)
    datum = DateField(model_attr='zasedanje__datum')
    text = CharField(document=True, use_template=True, template_name='search/indexes/zasedanja.txt')

site.register(Zapis, ZasedanjaIndex)
site.register(Seja, SejeIndex)