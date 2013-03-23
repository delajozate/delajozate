import pysolarized
from django.conf import settings
import datetime
import sys

search_register = {}
search_register_by_name = {}

def get_solr_backend():
    solr = pysolarized.Solr(settings.SOLR_URL)
    return solr

def register_search(model, model_name, searchmodel):
    global search_register, search_register_by_name
    modl = search_register_by_name.setdefault(model_name, model)
    search_register.setdefault(modl, searchmodel)
    return modl

class SearchBase(type):
    def __new__(cls, name, bases, attrs):
        new_class = super(SearchBase, cls).__new__(cls, name, bases, attrs)
        parents = [b for b in bases if isinstance(b, SearchBase)]
        if not parents:
            return new_class

        modl = attrs.get('model')
        new_class.model_name = '%s.%s' % (modl._meta.app_label, modl.__name__)
        return register_search(modl, new_class.model_name, new_class)

class SearchModel(object):
    __metaclass__ = SearchBase

    model = None
    template_name = None
    index_fields = None
    hilight = None

    def get_queryset(self):
        return self.model.objects.all()

    def index(self, items=None):
        solr = get_solr_backend()
        meta = self.model._meta

        if items is None:
            items = self.get_queryset()
        try:
            num_items = items.count()
        except Exception, e:
            print e
            num_items = len(items)
        for n, obj in enumerate(items):
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
            if self.hilight is not None:
                v = getattr(obj, self.hilight)
                if callable(v):
                    v = v()
                doc_list.append(('vsebina', v))
            doc = dict(doc_list)
            doc.update({
                "id": "%s.%s" % (self.model_name, obj.pk),
                "tip": self.model_name,
                #"ime": unicode(obj),
            })
            solr.add(doc)
            if n % 1000 == 0:
                sys.stderr.write('\rDone: %.2f%% (%s of %s)' % ((n+1)*100.0/num_items, n, num_items))
                sys.stderr.flush()
        solr.commit()
        sys.stderr.write('\n')

