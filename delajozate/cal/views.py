from icalendar import Calendar, Event as IEvent
import datetime
from django.http import HttpResponse
from datetime import date
from models import Event

NUM_EVENTS = 50

def calendar(request):
    pass

def ical(request):

    cal = Calendar()
    
    cal.add('prodid', '-//%s Events Calendar//%s//' % ("URNIK", "DELAJOZATE"))
    cal.add('version', '2.0')

    site_token = "DELAJOZATE"
    
    events = Event.objects.order_by('start').reverse()[:NUM_EVENTS]
    for e in events:

        ical_event = IEvent()
        ical_event.add('summary', e.title)
        ical_event.add('dtstart', e.start)
        ical_event.add('dtend', e.end)
        ical_event.add('location', e.location)
        ical_event.add('description', e.category + " " + str(e.url))
        ical_event['uid'] = '%d.event.events.%s' % (e.id, site_token)
        cal.add_component(ical_event)
    
    response = HttpResponse(cal.to_ical(), mimetype="text/calendar")
    response['Content-Disposition'] = 'attachment; filename=%s.ics' % "urnik"
    return response
