import pysolarized
from django.conf import settings
import datetime

search_register = {}

def get_solr_backend():
    solr = pysolarized.Solr(settings.SOLR_URL)
    return solr

def register_search(model, searchmodel):
    global search_register
    #print 'registering', model._meta.app_label, model.__name__
    return search_register.setdefault(model, searchmodel)

class SearchBase(type):
    def __new__(cls, name, bases, attrs):
        new_class = super(SearchBase, cls).__new__(cls, name, bases, attrs)
        parents = [b for b in bases if isinstance(b, SearchBase)]
        if not parents:
            return new_class

        modl = attrs.get('model')
        return register_search(modl, new_class)

class SearchModel(SearchBase):
    __metaclass__ = SearchBase

    model = None
    index_fields = None

    def __init__(self, *args, **kwargs):
        print 'Model __init__'

    @classmethod
    def index(self):
        solr = get_solr_backend()
        meta = self.model._meta
        model_name = '%s.%s' % (meta.app_label, self.model.__name__)
        for obj in self.model.objects.all():
            doc_list = []
            for k in self.index_fields:
                val = getattr(obj, k)
                if callable(val):
                    val = val()
                if isinstance(val, (datetime.datetime, datetime.date)):
                    solr_val = pysolarized.to_solr_date(val)
                    solr_key = 'datum_%s' % k
                else:
                    solr_val = unicode(val)
                    solr_key = 'str_%s' % k
                doc_list.append((solr_key, solr_val))
            doc = dict(doc_list)
            doc.update({
                "id": "%s.%s" % (model_name, obj.pk),
                "tip": model_name,
                #"ime": unicode(obj),
            })
            solr.add(doc)
        solr.commit()

