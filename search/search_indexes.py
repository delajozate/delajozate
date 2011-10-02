# Sets search index models for haystack
import haystack
from haystack.fields import CharField, DateField, IntegerField
from haystack.sites import site
from dz.models import Oseba, Stranka, Odbor, Skupina
from search.models import Zapis, Seja

class OsebeIndex(haystack.indexes.SearchIndex):
    rojstni_dan = DateField(null=True, model_attr='rojstni_dan')
    text = CharField(document=True, use_template=True, template_name='search/indexes/osebe.txt')

    def prepare(self, obj):
        data = super(OsebeIndex, self).prepare(obj)
        data['boost'] = 1.2     # Osebe imajo dodaten boost pri iskanju da pridejo na vrh
        return data

class StrankeIndex(haystack.indexes.SearchIndex):
    text = CharField(document=True, use_template=True, template_name='search/indexes/stranke.txt')

    def prepare(self, obj):
        data = super(StrankeIndex, self).prepare(obj)
        data['boost'] = 1.2
        return data

class OdboriIndex(haystack.indexes.SearchIndex):
    text = CharField(document=True, use_template=True, template_name='search/indexes/odbori.txt')

class SkupineIndex(haystack.indexes.SearchIndex):
    text = CharField(document=True, use_template=True, template_name='search/indexes/skupine.txt')

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

site.register(Oseba, OsebeIndex)
site.register(Stranka, StrankeIndex)
site.register(Odbor, OdboriIndex)
site.register(Skupina, SkupineIndex)
site.register(Zapis, ZasedanjaIndex)
site.register(Seja, SejeIndex)