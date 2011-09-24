import search.views
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'import/$', search.views.do_import)
)
  