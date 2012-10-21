
from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'glasovanja.views.index',),
    url(r'^(?P<datum>\d\d\d\d-\d\d-\d\d)/(?P<id>\d+)/$', 'glasovanja.views.glasovanje'),
)
