from django.conf.urls.defaults import patterns, include, url

from delajozate.magnetogrami.models import Seja, Zasedanje

urlpatterns = patterns('',
	url(r'^$', 'iskanje.views.search'),
)
