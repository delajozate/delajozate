from django.conf.urls.defaults import patterns, include, url

from delajozate.magnetogrami.models import Seja, Zasedanje

urlpatterns = patterns('',
    url(r'^$', 'django.views.generic.simple.redirect_to', {'url': '/seje/dz/'}),
    url(r'^dz/$', 'delajozate.magnetogrami.views.seja_list',),
    url(r'^(?P<mdt>[^/]+)/(?P<mandat>\d+)-mandat/(?P<slug>[^/]+)/$', 
        'delajozate.magnetogrami.views.seja', name="magnetogrami_seja"),
    url(r'^(?P<mdt>[^/]+)/(?P<mandat>\d+)-mandat/(?P<slug>[^/]+)/(?P<datum_zasedanja>\d{4}-\d{2}-\d{2})/$',
        'delajozate.magnetogrami.views.seja', name="magnetogrami_zasedanje"),

)
