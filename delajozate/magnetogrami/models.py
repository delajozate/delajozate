import json
import os
import re
import dateutil.parser

from django.db import models, transaction, connection
from delajozate.dz.models import Oseba

GLASOVI = (
	('0', 'Proti'),
	('1', 'Za'),
	('2', 'Ni glasoval'),
)

class Seja(models.Model):
	naslov = models.CharField(max_length=2000)
	seja = models.CharField(max_length=255) # TODO: check validity
	slug = models.CharField(max_length=100, db_index=True)
	datum_zacetka = models.DateField(null=True)
	status = models.CharField(max_length=128)
	mandat = models.IntegerField()
	delovno_telo = models.CharField(max_length=20)
	url = models.URLField()

	class Meta:
		ordering = ('-mandat', '-datum_zacetka',)

	def __unicode__(self):
		return self.naslov

	def magnetogrami(self):
		return Zasedanje.objects.filter(seja=self).filter(models.Q(tip='magnetogram') | models.Q(tip='dobesednizapis')).select_related('seja')

class SejaInfo(models.Model):
	seja = models.ForeignKey(Seja)
	url = models.URLField()
	naslov = models.CharField(max_length=255)
	datum = models.DateField()


class Zasedanje(models.Model):
	seja = models.ForeignKey(Seja)
	naslov = models.CharField(max_length=255, null=True)
	datum = models.DateField(null=True)
	zacetek = models.TimeField(null=True)
	konec = models.TimeField(null=True)
	url = models.URLField(null=True)
	tip = models.CharField(max_length=255, null=True)

	class Meta:
		ordering = ('datum',)

	def __unicode__(self):
		return self.naslov + "(" + str(self.datum) + ")"


class Glasovanje(models.Model):
	seja = models.ForeignKey(Seja, null=True)
	ura = models.TimeField(null=True, blank=True)
	url = models.URLField(null=True)
	datum = models.DateField(null=True, blank=True)
	dokument = models.CharField(max_length=2000, null=True)
	naslov = models.CharField(max_length=2000, null=True)
	faza_postopka = models.CharField(max_length=255, null=True)


class Glas(models.Model):
	glasovanje = models.ForeignKey(Glasovanje, null=True)
	oseba = models.ForeignKey(Oseba, null=True)
	kvorum = models.BooleanField(default=False)
	glasoval = models.CharField(max_length=255, choices=GLASOVI)
	poslanec = models.CharField(max_length=128)


class Zapis(models.Model):
	zasedanje = models.ForeignKey(Zasedanje)
	seq = models.IntegerField()
	odstavki = models.TextField(null=True)
	govorec = models.CharField(max_length=255, null=True)
	govorec_oseba = models.ForeignKey(Oseba, null=True)

	class Meta:
		ordering = ('seq',)

	def __unicode__(self):
		if self.govorec:
			return self.govorec + ":" + self.odstavki[0:30]
		else:
			return self.odstavki[0:30]
	
	def clan_stranke():
		def fget(self):
			d = self.zasedanje.datum
			return self.govorec_oseba.stranke.filter(od__lte=d, do__gt=d)
		return (fget,)
	clan_stranke = property(*clan_stranke())

class GovorecMap(models.Model):
	govorec = models.CharField(max_length=200, unique=True, db_index=True)
	oseba = models.ForeignKey(Oseba)

	class Meta:
		verbose_name = u'Preslikava govorec-oseba'
		verbose_name_plural = u'Preslikave govorec-oseba'
	def __unicode__(self):
		return u'"%s" -> %s' % (self.govorec, self.oseba)
	
	def save(self, *args, **kwargs):
		super(GovorecMap, self).save(*args, **kwargs)
		
		# posodobi obstojece zapise
		with transaction.commit_on_success():
			transaction.set_dirty()
			
			cur = connection.cursor()
			cur.execute('''UPDATE %s SET govorec_oseba_id = %%s WHERE govorec = %%s''' % Zapis._meta.db_table, [self.oseba.id, self.govorec])
		

def _parse_time(time_string):
	try:
		parsed_time = time.strptime(time_string, "%H.%S")
	except:
		try:
			parsed_time = time.strptime(time_string, "%H")
		except:
			parsed_time = None

	if parsed_time:
		return time.strftime("%H:%S", parsed_time)
	else:
		return None


def seja_import_one(jsonData):
	govorci_fn = os.path.join(os.path.dirname(__file__), 'govorci.json')
	
	if jsonData['url'] in (
		'http://www.dz-rs.si/wps/portal/Home/deloDZ/seje/izbranaSejaDt?mandat=IV&seja=24%20025.%20Redna&uid=E55FDF1837852856C1257275002A20A7',
		'http://www.dz-rs.si/wps/portal/Home/deloDZ/seje/izbranaSejaDt?mandat=III&seja=18%20015.%20Redna&uid=BF0C1A3AD3AD5771C1256C7C0035B39E',
		'http://www.dz-rs.si/wps/portal/Home/deloDZ/seje/izbranaSejaDt?mandat=III&seja=20%20013.%20Redna&uid=0485BF77D1915B2AC1256AEA0027F57D',
		'http://www.dz-rs.si/wps/portal/Home/deloDZ/seje/izbranaSejaDt?mandat=III&seja=21%20005.%20Redna&uid=99B38E120CF33D2EC1256A3800491AA2',
		'http://www.dz-rs.si/wps/portal/Home/deloDZ/seje/izbranaSejaDt?mandat=III&seja=18%20002.%20Redna&uid=86E49857111C3DB0C1256A06004F1763',
		'http://www.dz-rs.si/wps/portal/Home/deloDZ/seje/izbranaSejaDt?mandat=II&seja=34%20004.%20Redna&uid=566456472D99E269C125687A002D0AEB',
		):
		# glupe skupne seje :/
		return
	with transaction.commit_on_success():
		mandat = int(jsonData.get('mandat'))
		naslov_seje = jsonData.get('naslov')
		dt = jsonData.get('delovno_telo')
		try:
			seja = Seja.objects.get(
				mandat=mandat,
				naslov=naslov_seje,
				delovno_telo=dt,
				)
		except Seja.DoesNotExist:
			seja = Seja(mandat=mandat, naslov=naslov_seje, delovno_telo=dt)
		
		match = re.search(u'((\d+)\s?\.\s*(redna|izredna|nujna|zasedanje))', naslov_seje, re.I)
		if not match:
			print [naslov_seje]
			print jsonData.get('url')
			print naslov_seje
			
		seja_slug = ('%s-%s' % match.groups()[1:]).lower()
		seja.slug = seja_slug
		try:
			seja.datum_zacetka = dateutil.parser.parse(jsonData.get('datum_zacetka'), dayfirst=True)
		except:
			seja.datum_zacetka = None
		seja.seja = match.group(1)
		seja.url = jsonData.get('url')
		seja.save()

		# jsonSeja objects
		for jsonSeja in jsonData.get('seja_info', []):
			sejaInfo = SejaInfo()
			sejaInfo.seja = seja
			sejaInfo.url = jsonSeja.get('url')
			sejaInfo.naslov = jsonSeja.get('naslov')
			sejaInfo.datum = dateutil.parser.parse(jsonSeja.get('datum'), dayfirst=True)
			sejaInfo.save()

		#Glasovanja
		for jsonGlasovanje in jsonData.get('glasovanja'):

			url = jsonGlasovanje.get("url")
			ura = jsonGlasovanje.get("ura")
			if not ura:
				ura = None
			if jsonGlasovanje.get('datum'):
				datum = dateutil.parser.parse(jsonGlasovanje.get('datum'), dayfirst=True)
			else:
				datum = None
			dokument = jsonGlasovanje.get("dokument")
			naslov = jsonGlasovanje.get("naslov")
			faza_postopka = jsonGlasovanje.get("faza postopka")

			try:
				glasovanje = Glasovanje.objects.get(
					seja=seja,
					ura=ura,
					url=url,
					datum=datum,
					dokument=dokument,
					naslov = naslov,
					faza_postopka=faza_postopka,
				)
			except Glasovanje.DoesNotExist:
				print datum
				print dokument
				print naslov
				glasovanje = Glasovanje()
				glasovanje.seja = seja
				glasovanje.ura = ura
				glasovanje.url = url
				glasovanje.datum = datum
				glasovanje.dokument = dokument
				glasovanje.naslov = naslov
				glasovanje.faza_postopka = faza_postopka
				glasovanje.save()

			for glas in jsonGlasovanje.get("glasovi"):
				poslanec = glas.get("poslanec")# .encode("utf-8")
				#print [poslanec]
				try:
					g = GovorecMap.objects.get(govorec=poslanec)
					oseba = g.oseba
				except GovorecMap.DoesNotExist:
					sp = poslanec.split()
					if len(sp) == 2:
						poslanec_r = u'%s %s' % (sp[1], sp[0])
						try:
							g = GovorecMap.objects.get(govorec=poslanec_r)
							oseba = g.oseba
						except GovorecMap.DoesNotExist:
							print '---- FAIL', [poslanec], poslanec
							oseba = None
					else:
						print '---- FAIL', [poslanec], poslanec
						oseba = None
				
				
				try:
					g = Glas.objects.get(
						glasovanje = glasovanje,
						poslanec = poslanec
					)
					if oseba is not None and g.oseba != oseba:
						# ob najdeni osebi shrani
						g.oseba = oseba
						g.save()
				except Glas.DoesNotExist:
					g = Glas(
						glasovanje=glasovanje,
						kvorum=glas.get('kvorum'),
						glasoval=glas.get('glasoval'),
						oseba=oseba,
						poslanec=poslanec
						)
					g.save()
			
		# Zasedanja
		for jsonZasedanje in jsonData.get('zasedanja'):
			for jsonPovezava in jsonZasedanje.get('povezave'):
				datum = dateutil.parser.parse(jsonZasedanje.get('datum'), dayfirst=True)
				created = False
				try:
					zasedanje = Zasedanje.objects.get(
						datum=datum,
						seja=seja,
						)
				except Zasedanje.DoesNotExist:
					zasedanje = Zasedanje(
						datum=datum,
						seja=seja,
						)
					created = True

				if not created:
					continue
				if jsonPovezava.get('zacetek'):
					zasedanje.zacetek = _parse_time(jsonPovezava.get('zacetek'))
				if jsonPovezava.get('konec'):
					zasedanje.konec = _parse_time(jsonPovezava.get('konec'))

				zasedanje.tip = jsonPovezava.get('tip')
				zasedanje.naslov = jsonPovezava.get('naslov')
				zasedanje.url = jsonPovezava.get('url')
				zasedanje.save()

				cursor = connection.cursor()
				count = 0
				keys = ['seq', 'zasedanje_id', 'govorec', 'govorec_oseba_id', 'odstavki']

				values = []
				for jsonOdsek in jsonPovezava.get('odseki'):
					for jsonZapis in jsonOdsek.get('zapisi'):
						govorec = jsonZapis.get('govorec')
						if govorec is not None:
							govorec = govorec.strip()
							m = re.match('^(.*)\s\(PS \w{2,5}\)$', govorec)
							if m:
								govorec = m.group(1)
						try:
							oseba_id = GovorecMap.objects.get(govorec=govorec).oseba.id
						except GovorecMap.DoesNotExist:
							oseba_id = None

						for ods in jsonZapis.get('odstavki'):
							values.extend([
								count,
								zasedanje.id,
								govorec,
								oseba_id,
								ods,
								])
							count += 1

				params = values
				onerowtempl = '(' + ', '.join(['%s'] * len(keys)) + ')'
				all_rows_template = ', '.join([onerowtempl] * (len(params) / len(keys)))
				sql = '''INSERT INTO %s (%s) VALUES %s''' % (
					Zapis._meta.db_table,
					', '.join(keys),
					all_rows_template)
				if params:
					cursor.execute(sql, params)
		if seja.datum_zacetka is None:
			# use as an alternative
			try:
				seja.datum_zacetka = Zasedanje.objects.filter(seja=seja).order_by('-datum')[0].datum
			except:
				pass
		seja.save()
