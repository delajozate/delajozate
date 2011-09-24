import csv
from dz.models import Mandat

mandates = Mandat.objects.all()

# Specify source file
source_file = 'C:/Development/Projects/delajozate/poslanci_data/poslanci_clean.csv'

rdr = csv.reader(open(source_file))

for rec in rdr:
	print rec