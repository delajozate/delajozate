from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('cal.views',
    #url(r'^$', 'calendar', name='calendar'),
    url(r'^ical/$', 'ical', name='ical'),
    
)

