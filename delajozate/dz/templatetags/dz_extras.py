from django import template
from django.template.defaultfilters import stringfilter

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
