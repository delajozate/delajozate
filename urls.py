from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'delajozate.views.home', name='home'),
    # url(r'^delajozate/', include('delajozate.foo.urls')),
    url(r'^seje/(?P<mdt>[^/]+)/(?P<mandat>\d+)-mandat/(?P<slug>[^/]+)/$', 
        'delajozate.magnetogrami.views.seja', name="magnetogrami_seja"),
    url(r'^seje/(?P<mdt>[^/]+)/(?P<mandat>\d+)-mandat/(?P<slug>[^/]+)/(?P<datum_zasedanja>\d{4}-\d{2}-\d{2})/$',
        'delajozate.magnetogrami.views.seja', name="magnetogrami_zasedanje"),
    url(r'^', include('dz.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
