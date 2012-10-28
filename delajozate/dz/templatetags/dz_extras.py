import datetime
import re

from django import template
from django.template.defaultfilters import stringfilter
from django.db.models import Q

from delajozate.dz.models import Mandat

register = template.Library()

@register.filter
def slopluralize(num, suffixes):
	suf = suffixes.split(",")
	if type(num) != int or len(suf) < 4:
		return ""
	num = num % 100
	if num == 1:
		return suf[0]
	elif num == 2:
		return suf[1]
	elif num in [3,4]:
		return suf[2]
	else:
		return suf[3]
	
	
@register.filter
def get_item(dictionary, key):
	return dictionary.get(key)

@register.filter
def datum_filter(value, arg):
	"""
	Filters the clan stranke queryset by date given, to get the membership.
	Can also give "today" as arg.
	"""
	if isinstance(arg, (tuple, list)):
		arg = arg[0]
	if arg == "today":
		arg = datetime.date.today()
	
	low = arg
	high = arg
	if isinstance(arg, basestring):
		match = re.match('^(\d+)-mandat', arg)
		if match:
			m = Mandat.objects.get(st=match.group(1))
			low = m.od
			high = m.do
	
	#print 'A', value, low, high
	#print 'B', value.filter(od__gte=low, do__lte=high)
	#print 'C', value.filter(Q(od__lte=low, do__gt=low) | Q(od__lte=high, do__gt=high) | Q(od__lte=low, do__gt=high))
	clanstvo = list(value.filter(
		Q(od__lte=low, do__gt=low) |   # crosses lower boundary
		Q(od__lte=high, do__gt=high) | # crosses upper boundary
		Q(od__lte=low, do__gt=high)))  # or is in between
	
	return clanstvo
	