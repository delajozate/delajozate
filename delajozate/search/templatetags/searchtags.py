from django import template
#from delajozate.search.simple import search_register
from pysolarized import from_solr_date

register = template.Library()

def search_template(value):
    return 'item_%s.html' % (value.lower(),)
register.filter('search_template', search_template)

def solrdate2date(value):
    return from_solr_date(value)
register.filter('solrdate2date', solrdate2date)

def dictget(value, key):
    return value.get(key)
register.filter('dictget', dictget)