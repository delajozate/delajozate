from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('dz.views',
	url(r'^stranke/json/', 'stranke_json', name='stranke_json'),
    url(r'^poslanec/(?P<slug>[A-Za-z0-9-_]{96})/$', 'poslanec', name='poslanec'),
    url(r'^$', 'home', name='home'),
)
