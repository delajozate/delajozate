from django.conf.urls.defaults import patterns, include, url

from delajozate.magnetogrami.models import Seja

seja_list = {
    'queryset': Seja.objects.all().order_by('-mandat', '-datum_zacetka'),
    }

urlpatterns = patterns('',
    url(r'^$', 'django.views.generic.simple.redirect_to', {'url': '/seje/dz/'}),
    url(r'^dz/$', 'django.views.generic.list_detail.object_list', seja_list),
    url(r'^(?P<mdt>[^/]+)/(?P<mandat>\d+)-mandat/(?P<slug>[^/]+)/$', 
        'delajozate.magnetogrami.views.seja', name="magnetogrami_seja"),
    url(r'^(?P<mdt>[^/]+)/(?P<mandat>\d+)-mandat/(?P<slug>[^/]+)/(?P<datum_zasedanja>\d{4}-\d{2}-\d{2})/$',
        'delajozate.magnetogrami.views.seja', name="magnetogrami_zasedanje"),

)
