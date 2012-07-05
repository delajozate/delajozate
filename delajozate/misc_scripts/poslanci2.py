#!/usr/bin/env python

# XXX FIXME needs fixing
# I'm not guaranteeing all the IDs are the same after the stranke cleanup.
# by Zejn, 7. nov. 2011

import sys
sys.path.append("..")

from django.template.defaultfilters import slugify

from delajozate.dz.models import Oseba, Stranka, ClanStranke
from delajozate.temporal import END_OF_TIME

import csv
import re
from datetime import date
from pprint import pprint

start = {
	'1992-1996': date(1992, 12, 23),
	'1996-2000': date(1996, 11, 27),
	'2000-2004': date(2000, 10, 22),
	'2004-2008': date(2004, 10, 22)
}

end = {
	'1992-1996': date(1996, 11, 27),
	'1996-2000': date(2000, 10, 22),
	'2000-2004': date(2004, 10, 22),
	'2004-2008': date(2008, 10, 15)
}

mandates = {
	'1992-1996': 1,
	'1996-2000': 2,
	'2000-2004': 3,
	'2004-2008': 4,
	'2008-2011': 5,
}

stranke = {
	1: (date(1993, 5, 29), date(2005, 4, 2)),
	2: (date(2005, 4, 2), date(9999, 12, 31)),
	3: (date(1991, 3, 17), date(9999, 12, 31)),
	4: (date(2000, 8, 4), date(9999, 12, 31)),
	5: (date(2007, 10, 6), date(9999, 12, 31)),
	6: (date(1994, 3, 12), date(9999, 12, 31)),
	7: (date(1992, 6, 27), date(2000, 4, 15)),
	8: (date(1989, 11, 4), date(2000, 4, 15)),
	9: (date(2000, 4, 15), date(2002, 1, 31)),
	10: (date(2002, 1, 31), date(9999, 12, 31)),
	11: (date(1991, 5, 30), date(9999, 12, 31)),
	12: (date(1994, 4, 12), date(2000, 3, 16)),
	13: (date(1993, 3, 23), date(1994, 3, 12)),
	14: (date(2002, 2, 28), date(9999, 12, 31)),
	15: (date(1989, 2, 16), date(1990, 2, 24)),
	16: (date(1990, 2, 24), date(1996, 3, 23)),
	17: (date(2003, 9, 13), date(9999, 12, 31)),
	18: (None, date(1994, 4, 6)),
	19: (date(1994, 4, 6), None),
	20: (date(2000, 8, 8), date(2009, 7, 4)),
	21: (date(2009, 7, 4), date(9999, 12, 31)),
	22: (date(2004, 5, 8), date(2008, 1, 10)),
	23: (date(1994, 3, 12), date(9999, 12, 31)),
	24: (date(1991, 10, 13), date(1994, 3, 12)),
	25: (date(1989, 6, 11), date(9999, 12, 31)),
	26: (date(2000, 3, 16), date(2002, 2, 28)),
	27: (date(1996, 3, 23), date(2003, 9, 13)),
}

# 19 missing because of ID conflict; really belongs to 18; This means
# D->DS transitions are broken (probably missing second part)
stranke_id = {
	'as': [22],
	'd': [18],
	'desus': [11],
	'ds': [24, 23],
	'lds': [6],
	'nsi': [4],
	'sd': [2],
	'sds': [27, 17],
	'sdss': [16],
	'sdzs': [15],
	'skd': [8],
	'sls': [7, 10],
	'slsskd': [9],
	'sms': [20],
	'sms-zeleni': [21],
	'snd': [12],
	'sns': [3],
	'ssn': [26, 14],
	'zares': [5],
	'zeleni': [25],
	'zeleni-ess': [13],
	'zlsd': [1]
}

name_changes = {
	24: { 'to': 23, 'when': date(1994, 3, 12) },
	27: { 'to': 17, 'when': date(2003, 9, 13) }
}

pos_exceptions = {
	'tone-anderlic': 'anton-anderlic',
	'zmago-jelincic': 'zmago-jelincic-plemeniti',
	'anton-tone-partljic': 'tone-partljic',
	'ivan-janez-jansa': 'janez-jansa',
	'jasa-zlobec-l': 'jasa-zlobec-lukic',
	'majda-sirca': 'majda-sirca-ravnikar'
}

# Members are not members of a party
party_exceptions = set([
	"ssp",
	"samostojna-poslanka",
	"samostojni-poslanec",
	"nepovezani-poslanec",
	"np"
])

special = set([
	"poslanec-italijanske-narodne-skupnosti",
	"poslanka-madzarske-narodne-skupnosti"
])


name_re = re.compile('^((?:dr|mag)\.)?\s*(\S+)\s*(.+?)(\*)?$', re.I)


def find_person(name_slug):
	if name_slug in pos_exceptions:
		name_slug = pos_exceptions[name_slug]
	try:
		return Oseba.objects.get(slug=name_slug)
	except:
		return None

def get_slug(value):
	'''
	Get slug for a person without titles
	'''
	name = value.strip()
	if name.lower()[:3] == "dr.":
		name = name[3:].strip()
	if name.lower()[:4] == "mag.":
		name = name[4:].strip()
	name_slug = slugify(name)
	if name_slug in pos_exceptions:
		name_slug = pos_exceptions[name_slug]
	return name_slug


def get_period_membership(raw_string, period):
	'''
	Parse party membership in a given period

	Returns a list of membership dicts:
		- from (when membership started)
		- to (when ended)
		- party (party ID)

	Note: party can also be:
		- 0 (not a member of any)
		- -1 (minority representative)
		- -2 (unknown)
	'''
	period_start = start[period]
	period_end = end[period]
	known_date = period_start
	memberships = []

	# First parse -> (we have exact dates)
	# Then parse rest by , (put None)
	# Note: party can change name (gets new ID)
	party = None
	parts = [ x.strip() for x in raw_string.strip().lower().split("->") ]
	for part in parts:
		if party: # From previous iteration. Set to the one that changed name
			if party in stranke_id:
				for pid in stranke_id[party]:
					pp = stranke[pid]
					if (not pp[0] or pp[0] < known_date) and pp[1] > known_date: # Found it, already added though
						known_date = pp[1]
						memberships[-1]['to'] = known_date
						memberships[-1]['party'] = pid
			else: # Unaccounted coalitions (ZL, Zeleni/LDS)
				pass

		parties = [ slugify(x.strip()) for x in part.split(",") ]
		for p in parties:
			if party: # Name change: new name
				if p in stranke_id:
					for pid in stranke_id[p]:
						pp = stranke[pid]
						if pp[0] == known_date and (not pp[1] or pp[1] > known_date): # Found it
							memberships.append({
								'party': pid,
								'from': known_date,
								'to': None
							})
				else: # Unaccounted coalitions (ZL, Zeleni/LDS)
					pass
				party = None
			else:
				if p in stranke_id:
					memberships.append({
						'party': stranke_id[p][0],
						'from': None,
						'to': None
					})
				elif p in special: # Minority
					memberships.append({ 'party': -1,
						'from': period_start,
						'to': period_end
					})
				elif p in party_exceptions:
					# Not a party member in this period; still add marker
					memberships.append({ 'party': 0, 'from': None, 'to': None })
				else: # Coalitions: ZL or Zeleni/LDS; Don't know how to handle yet
					memberships.append({ 'party': -2, 'from': None, 'to': None })
		party = p
	if len(memberships):
		if not memberships[0]['from']:
			memberships[0]['from'] = period_start
		if not memberships[-1]['to']:
			memberships[-1]['to'] = period_end
	return memberships

def create_time_helper(members, s, e):
	# Set 'to' and 'from' for helpers for easier handling of time
	helpers = []
	for it in members:
		item = it.copy()
		if not item['from']:
			item['from'] = s
		else:
			s = item['from']
		if item['to']:
			s = item['to']
		helpers.append(item)
	helpers.reverse()
	for item in helpers:
		if not item['to']:
			item['to'] = e
		else:
			e = item['to']
	return helpers

def fix_party_name_change(memberships):
	fixed = []
	period_start = None
	period_end = None
	period = None
	party = None
	helpers = []
	rmemberships = memberships[:]

	# Set 'to' and 'from' for helpers for easier handling of time
	helpers = create_time_helper(memberships, start['1992-1996'], end['2004-2008'])

	# Now get to it
	rmemberships.reverse()
	while rmemberships:
		period = rmemberships.pop()
		helper = helpers.pop()

		if period['party'] > 0 and period['party'] in name_changes: # possible candidate for name change
			pid = period['party']
			change_date = name_changes[pid]['when']
			if helper['from'] > change_date:
				period['party'] = name_changes[pid]['to']
				fixed.append(period)
			else:
				if helper['to'] > change_date: # ...and helper['from'] < change_date => split
					new_period = {
						'party': name_changes[pid]['to'],
						'from': name_changes[pid]['when'],
						'to': helper['to']
					}
					period['to'] = name_changes[pid]['when']
					fixed.append(period)
					fixed.append(new_period)
				else: # Before change
					fixed.append(period)
		else:
			fixed.append(period)
	fixed.reverse()
	return fixed

def clean_membership(memberships):
	'''
	Merge overlapping intervals
	'''
	clean = []
	period = None
	rmemberships = memberships[:]

	while rmemberships:
		new_period = rmemberships.pop()
		if not period:
			period = new_period
			continue

		if period['party'] == new_period['party'] and period['to'] == new_period['from']:
			period['to'] = new_period['to']
		else:
			clean.append(period)
			period = new_period

	clean.append(period)
	return clean

def save_membership(name_slug, memberships):
	'''
	Save memberships. Return True if person exists and False otherwise.
	'''
	person = find_person(name_slug)

	if person:
		for m in memberships:
			party_id = m['party'] if m['party'] > 0 else None
			# TODO: Change database so it can handle null 'from'
			ClanStranke.objects.create(oseba=person, stranka_id=party_id, od=m['from'], do=m['to'])
		return True
	return False

def run(filepath):
	rdr = csv.reader(open(filepath))
	poslanci = {}
	today = date.today()

	for rec in rdr:
		name_slug = get_slug(rec[1])
		poslanci.setdefault(name_slug, [])
		poslanci[name_slug] += get_period_membership(rec[2], rec[0])

	for pos in poslanci:
		if poslanci[pos][-1]['to'] > today:
			poslanci[pos][-1]['to'] = END_OF_TIME
		poslanci[pos] = fix_party_name_change(poslanci[pos])
		poslanci[pos] = clean_membership(poslanci[pos])
		# save_membership(pos, poslanci[pos])

	# Test cases
	print 'roberto-battelli'
	pprint(poslanci['roberto-battelli'])
	print 'anton-anderlic'
	pprint(poslanci['anton-anderlic'])
	print
	print 'janez-jansa'
	pprint(poslanci['janez-jansa'])
	print
	print 'ljerka-bizilj'
	pprint(poslanci['ljerka-bizilj'])
	print 'stefan-matus'
	pprint(poslanci['stefan-matus'])
	print 'france-bucar'
	pprint(poslanci['france-bucar'])


if __name__ == '__main__':
	run(sys.argv[1])
