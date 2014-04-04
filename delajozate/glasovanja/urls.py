from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'glasovanja.views.index',),
    url(r'^(?P<datum>\d\d\d\d-\d\d-\d\d)/(?P<ura>\d\d:\d\d:\d\d)/$', 'glasovanja.views.glasovanje'),
    url(r'^(?P<datum>\d\d\d\d-\d\d-\d\d)/(?P<pk>\d+)/$', 'glasovanja.views.glasovanje'),
)
