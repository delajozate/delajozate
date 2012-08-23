from django.conf.urls.defaults import patterns, include, url

from delajozate.magnetogrami.models import Seja, Zasedanje

urlpatterns = patterns('',
	url(r'^$', 'delajozate.magnetogrami.views.tipi_sej',),
	url(r'^(?P<mdt>[^/]+)/$', 'delajozate.magnetogrami.views.seja_list',),
	url(r'^(?P<mdt>[^/]+)/(?P<mandat>\d+)-mandat/$', 'delajozate.magnetogrami.views.seja_list',),
	url(r'^(?P<mdt>[^/]+)/(?P<mandat>\d+)-mandat/(?P<slug>[^/]+)/$', 
		'delajozate.magnetogrami.views.seja', name="magnetogrami_seja"),
	url(r'^(?P<mdt>[^/]+)/(?P<mandat>\d+)-mandat/(?P<slug>[^/]+)/(?P<datum_zasedanja>\d{4}-\d{2}-\d{2})/$',
		'delajozate.magnetogrami.views.seja', name="magnetogrami_zasedanje"),
	url(r'^(?P<mdt>[^/]+)/(?P<mandat>\d+)-mandat/(?P<slug>[^/]+)/(?P<datum_zasedanja>\d{4}-\d{2}-\d{2})/p(?P<odstavek>\d+)/$',
		'delajozate.magnetogrami.views.citat', name="magnetogrami_citat"),
	

)
