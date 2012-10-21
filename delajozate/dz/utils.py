
from dz.models import ClanStranke

def get_poslanci(filters=None, mandat=None):
	if not filters:
		filters = {}
	
	# mandati & dnevi / osebo
	osebe_mandati_dict, osebe_dni_dict =  get_osebe_data()
	
	# vsi clani, oseba samo prvic, clanstvo torej zadnje
	poslanci = []
	existing = set([])
	for clanstvo in ClanStranke.objects.filter(**filters).select_related('oseba', 'stranka').order_by('oseba__priimek', 'oseba__ime', '-od'):
		oseba = clanstvo.oseba
		pk = oseba.pk
		if pk not in existing:
			if not mandat or mandat in osebe_mandati_dict[pk]:
				poslanci.append({
					'oseba': oseba,
					'stranka': clanstvo.stranka,
					'poslanskih_dni': osebe_dni_dict[pk],
					'mandati': osebe_mandati_dict[pk],
					'short': True
				})
		existing.add(pk)
	
	return poslanci
	
