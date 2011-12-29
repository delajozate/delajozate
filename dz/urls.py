from django.conf.urls.defaults import patterns, include, url

from delajozate.dz.models import Oseba
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('dz.views',
	url(r'^stranke/json/', 'stranke_json', name='stranke_json'),
    url(r'^poslanci/(?P<slug>[A-Za-z0-9-_]{96})/$', 'poslanec', name='poslanec'),
    url(r'^poslanci/$', 'poslanci_list'),
    url(r'^$', 'home', name='home'),
)

urlpatterns += patterns('django.views.generic',
    url(r'^poslanci/(?P<slug>[^/]+)/$', 'list_detail.object_detail', {'queryset': Oseba.objects.all()}),
)
