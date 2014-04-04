from django.conf.urls import patterns, include, url

urlpatterns = patterns('cal.views',
    #url(r'^$', 'calendar', name='calendar'),
    url(r'^ical/$', 'ical', name='ical'),
    
)

