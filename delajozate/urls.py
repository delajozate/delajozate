from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'delajozate.views.home', name='home'),
    # url(r'^delajozate/', include('delajozate.foo.urls')),
    url(r'^seje/', include('magnetogrami.urls')),
    url(r'^glasovanja/', include('glasovanja.urls')),
    url(r'^iskanje/', include('haystack.urls')),
    url(r'^koledar/', include('cal.urls')),
    url(r'^', include('dz.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
