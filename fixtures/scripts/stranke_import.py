import csv
import datetime
import dateutil.parser
from delajozate.dz.models import Stranka

# Specify source file
source_file = 'csv_fixtures/stranke_zgodovina.csv'


Stranka.objects.all().delete()

rdr = csv.reader(open(source_file))
for n, row in enumerate(rdr):
	if n > 1:
		if len(row) < 10:
			row = row + [None]*(10-len(row))

		row = map(lambda x:x or None, row)
		#print row
		id, parent_id, ime, okrajsava, od, do, maticna, davcna, opombe, url = row

		if od is not None:
			od = dateutil.parser.parse(od)
		if do is not None:
			do = dateutil.parser.parse(do)

		stranka = Stranka(
				id=id,
				ime=ime,
				maticna=maticna,
				davcna=davcna,
				okrajsava=okrajsava,
				od=od,
				do=do,
				email=None,
				barva=None,
				spletna_stran=url,
				opombe=opombe)
		stranka.save()

rdr = csv.reader(open(source_file))
for n, row in enumerate(rdr):
	if n > 1:
		id, parent_id = row[:2]
		if parent_id:
			print id, parent_id
			parents = map(int, parent_id.split(','))
			stranka = Stranka.objects.get(pk=id)
			for parent in parents:
				pstranka = Stranka.objects.get(pk=parent)
				stranka.nastala_iz.add(pstranka)

			stranka.save()
