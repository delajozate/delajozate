from django.conf.urls.defaults import patterns, include, url

from dz.models import Oseba
from dz.views import PoslanciList, GlasovanjaList, TweetList
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('dz.data_check',
    url(r'^datacheck/$', 'data_check', name='data_check'),
)

urlpatterns += patterns('dz.views',
    #url(r'^stranke/', 'stranke_list', name='stranke_list'),
    url(r'^stranke/json/', 'stranke_json', name='stranke_json'),

    url(r'^osebe/(?P<slug>[A-Za-z0-9-_]+)/$', 'poslanec', name='poslanec'),
    url(r'^osebe/(?P<slug>[A-Za-z0-9-_]+)/glasovanja/$', GlasovanjaList.as_view(),
        name='poslanec_glasovanja'),
    url(r'^osebe/(?P<slug>[A-Za-z0-9-_]+)/tweets/$', TweetList.as_view(),
        name='poslanec_twitter'),
    url(r'^poslanci/(?P<mandat>danes|\d+-mandat)/$', PoslanciList.as_view(), name='poslanci_list'),
    url(r'^robots.txt$', 'robots'),
    url(r'^$', 'home', name='home'),
)

urlpatterns += patterns('django.views.generic',
    url(r'^poslanci/$', 'simple.redirect_to', {'url': '/poslanci/danes/'}),
)
