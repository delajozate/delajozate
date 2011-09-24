import csv
import datetime
from dz.models import Mandat, Oseba, Poslanec

mandates = Mandat.objects.all()

# Specify source file
source_file = 'C:/Development/Projects/delajozate/poslanci_data/poslanci_clean.csv'

rdr = csv.reader(open(source_file))

#Store the mandates
mandates = {}

def get_mandate(mandate_number):
	if mandate_number not in mandates:
		mandates[mandate_number] = Mandat.objects.get(st=mandate_number)
	return mandates[mandate_number]


for rec in rdr:
	first_name = rec[2]
	last_name = rec[3]
	persons = Oseba.objects.filter(ime=first_name, priimek=last_name)

	# Get person if it exists or create a new one
	if len(persons):
		person = persons[0]
	else:
		person = Oseba.objects.create(ime=first_name, priimek=last_name)

	from_date = rec[5]
	to_date = rec[6]
	mandate = rec[7]

	Poslanec.objects.create(oseba=person, od=datetime.datetime.strptime(from_date, '%Y-%m-%d'), do=datetime.datetime.strptime(to_date, '%Y-%m-%d'), mandat=get_mandate(mandate))
