from icalendar import Calendar, Event
from datetime import datetime
from django.http import HttpResponse
from datetime import date

def ical(request):

    cal = Calendar()
    
    cal.add('prodid', '-//%s Events Calendar//%s//' % ("NAME", "DOMAIN"))
    cal.add('version', '2.0')

    site_token = "TOKEN"

    ical_event = Event()
    ical_event.add('summary', "SUMM")
    ical_event.add('dtstart', date.today())
    ical_event.add('dtend', date.today())
    ical_event.add('dtstamp', date.today())
    ical_event['uid'] = '%d.event.events.%s' % (123, site_token)
    cal.add_component(ical_event)
    cal.add_component(ical_event)
    cal.add_component(ical_event)

    response = HttpResponse(cal.to_ical(), mimetype="text/calendar")
    response['Content-Disposition'] = 'attachment; filename=%s.ics' % "KOLEDAR"
    print str(cal.to_ical())
    return response