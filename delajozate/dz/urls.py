from django.conf.urls.defaults import patterns, include, url

from delajozate.dz.models import Oseba
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('dz.data_check',
	url(r'^datacheck/$', 'data_check', name='data_check'),
)

urlpatterns += patterns('dz.views',
	#url(r'^stranke/', 'stranke_list', name='stranke_list'),
	url(r'^stranke/(?P<stranka_id>\d+)/', 'stranka', name='stranka'),
	url(r'^stranke/json/', 'stranke_json', name='stranke_json'),
	
	url(r'^osebe/(?P<slug>[A-Za-z0-9-_]+)/$', 'poslanec', name='poslanec'),
	url(r'^poslanci/(?P<mandat>danes|\d+-mandat)/$', 'poslanci_list'),
	url(r'^robots.txt$', 'robots'),
	url(r'^$', 'home', name='home'),
)

urlpatterns += patterns('django.views.generic',
	url(r'^poslanci/$', 'simple.redirect_to', {'url': '/poslanci/danes/'}),
)
