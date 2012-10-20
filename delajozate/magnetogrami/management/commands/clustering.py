import mdp
import numpy
import re
import datetime
import pylab

from django.core.management.base import NoArgsCommand
from django.db.models import Q
from dz.models import Mandat, Stranka
from magnetogrami.models import Glasovanje, GLASOVI

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

class Command(NoArgsCommand):

	def handle_noargs(self, **options):
		glasovanje_idx = 0
		stranke_vectors = {}

		st_glasovanj = Glasovanje.objects.count()

		for glasovanje in Glasovanje.objects.all():
			if glasovanje.datum is None:
				continue

			for glas in glasovanje.glas_set.select_related().all():
				clanstvo = datum_filter(glas.oseba.clanstvo(), glasovanje.datum)
				if len(clanstvo) == 0:
					continue

				stranka_id = clanstvo[0].stranka_id

				if stranka_id is None:
					continue

				if stranka_id not in stranke_vectors:
					print "Creating vector for stranka", stranka_id
					stranke_vectors[stranka_id] = numpy.zeros(st_glasovanj * 2)

				if glas.glasoval == "Proti":
					stranke_vectors[stranka_id][glasovanje_idx + 1] += 1
				elif glas.glasoval == "Za":
					stranke_vectors[stranka_id][glasovanje_idx] += 1

			glasovanje_idx += 2

		# Stack matrix
		vectors = []
		codebook = {}
		reverse_codebook = {}
		i = 0
		for stranka_id, vector in stranke_vectors.items():
			codebook[stranka_id] = len(vectors)
			reverse_codebook[i] = stranka_id
			i += 1
			vectors.append(vector)

		vector_matrix = numpy.vstack(vectors)
		print "Vector matrix:", vector_matrix.shape
		print vector_matrix
		pca = mdp.pca(vector_matrix.transpose(), output_dim=2).transpose()
		print "PCA:", pca.shape

		print pca[0]
		print pca[1]

		coordinates = {}

		min_x = 99999
		min_y = 99999

		for i in range(0, vector_matrix.shape[0]):
			x = vector_matrix[i].dot(pca[0])
			y = vector_matrix[i].dot(pca[1])

			if x < min_x: min_x = x
			if y < min_y: min_y = y

			coordinates[reverse_codebook[i]] = (x, y)

		for stranka_id, coords in coordinates.items():
			x, y = coords
			coordinates[stranka_id] = (x - min_x, y - min_y)

		x_s = [x for x, y in coordinates.values()]
		y_s = [y for x, y in coordinates.values()]

		pylab.scatter(x_s, y_s)

		for stranka_id, coords in coordinates.items():
			pylab.annotate(Stranka.objects.get(pk=stranka_id).ime, xy=coords, xytext=(-30, 10),  textcoords = 'offset points', ha = 'right', va = 'bottom')

		pylab.show()

