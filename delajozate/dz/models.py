# coding: utf-8
import datetime


from django.db import models, connection
from django.db.models import Q
from django.template.defaultfilters import slugify
from delajozate.temporal import END_OF_TIME


FUNKCIJE = (
	('poslanec', 'Poslanec/ka'),
	('clan', 'Član'),
	('predsednik', 'Predsednik'),
	('podpredsednik', 'Podpredsednik'),
)

def null_date(date):
	if date == END_OF_TIME:
		return None
	return date

ORG_CHOICES = (
	(1, 'stranka'),
	(2, 'skupina'),
	(3, 'drzavnizbor'),
	(4, 'delovnotelo'),
)

class Organizacija(models.Model):
	tip = models.IntegerField(choices=ORG_CHOICES)

	def type(self):
		return self.get_tip_display()

	def __unicode__(self):
		t = self.type()
		return u"[%s] %s" % (t, getattr(self, t)) if t != "" else None

	def value(self):
		return getattr(self, self.type())



class Oseba(models.Model):
	ime = models.CharField(max_length=32)
	priimek = models.CharField(max_length=64)
	slug = models.SlugField(max_length=96)
	email = models.EmailField(max_length=64, blank=True)
	rojstni_dan = models.DateField(blank=True, null=True)
	dan_smrti = models.DateField(blank=True, null=True)
	slika = models.CharField(max_length=200, blank=True)
	vir_slike = models.CharField(max_length=200, blank=True)
	spletna_stran = models.URLField(blank=True)
	twitter = models.CharField(max_length=32, blank=True)
	facebook = models.URLField(blank=True)
	podatki_preverjeni = models.BooleanField(default=False)
	opombe = models.TextField(blank=True)

	class Meta:
		ordering = ('priimek', 'ime')
		verbose_name_plural = u'Osebe'

	def __unicode__(self):
		return u'%s %s' % (self.ime, self.priimek)

	def slika_or_default(self):
		if self.slika:
			return self.slika
		return '/static/img/unknown.png'

	def slika_vir(self):
		if self.slika:
			return self.vir_slike
		return 'http://www.flickr.com/photos/marypaulose/295058238/sizes/z/in/photostream/'

	def st_mandatov(self):
		return self.pozicija_set.filter(tip='poslanec').count()

	def poslanskih_dni(self):
		cur = connection.cursor()
		sql = '''SELECT SUM(CASE WHEN F.do > NOW()::date THEN NOW()::date ELSE F.do END - F.od) AS st_dni FROM dz_pozicija F WHERE oseba_id = %s AND tip = 'poslanec' '''
		params = [self.pk]
		cur.execute(sql, params)
		return cur.fetchall()[0][0]

	def clanstvo(self, day=None):
		if day:
			# take from dz_extras.py - datum_filter, unify me
			low = high = day
			clanstvo = list(self.pozicija_set.filter(
				Q(od__lte=low, do__gt=low) |   # crosses lower boundary
				Q(od__lte=high, do__gt=high) | # crosses upper boundary
				Q(od__lte=low, do__gt=high)).filter( organizacija__stranka__gt=0).select_related('organizacija', 'organizacija__stranka'))  # or is in between
			return clanstvo

		return self.pozicija_set.filter(organizacija__stranka__gt=0).order_by('-do').select_related('organizacija', 'organizacija__stranka')

	def funkcije(self):
		return self.pozicija_set.exclude(organizacija=None).order_by('-do').select_related('organizacija', 'organizacija__drzavnizbor')

	def delovna_telesa(self):
		return self.pozicija_set.filter(organizacija__delovnotelo__gt=0).order_by('od').select_related('organizacija', 'organizacija__delovnotelo')

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slug = slugify("%s %s" % (self.ime, self.priimek))
			count = 2
			while Oseba.objects.filter(slug=self.slug).count():
				self.slug = "%s-%d" % (slug, count)
				count += 1
		super(Oseba, self).save(*args, **kwargs)

	def display(self):
		return u'%s %s' % (self.ime, self.priimek)


class Tweet(models.Model):
	tweet_id = models.BigIntegerField(blank=False, null=True)
	text = models.CharField(max_length=250)
	oseba = models.ForeignKey(Oseba)
	created_at = models.DateTimeField()

	class Meta:
		ordering = ('-created_at',)

	def __unicode__(self):
		return self.text

class Stranka(models.Model):
	# kako modelirat kontinuiteto stranke, kadar se preimenuje?
	nastala_iz = models.ManyToManyField("self", related_name="spremenila_v", symmetrical=False, blank=True)
	ime = models.CharField(max_length=128)
	maticna = models.CharField(max_length=10, blank=True)
	davcna = models.CharField(max_length=10, blank=True)
	okrajsava = models.CharField(max_length=16)
	email = models.EmailField(max_length=64, blank=True)
	barva = models.CharField(max_length=6, blank=True)
	od = models.DateField(null=True)
	do = models.DateField(null=True, default=END_OF_TIME)
	spletna_stran = models.URLField(blank=True)
	twitter = models.CharField(max_length=32, blank=True)
	facebook = models.URLField(blank=True)
	podatki_preverjeni = models.BooleanField(default=False)
	opombe = models.TextField(blank=True)
	organizacija = models.OneToOneField(Organizacija, null=True)

	def save(self, *args, **kwargs):
		if not self.organizacija_id:
			self.organizacija = Organizacija.objects.create()
		super(Stranka, self).save(*args, **kwargs)

	class Meta:
		verbose_name_plural = u'Stranke'
		ordering = ('-do', 'ime')

	def __unicode__(self):
		return u'%s (%s)%s' % (self.ime, self.okrajsava, self.do != END_OF_TIME and u'\u271d' or u'')

	def display(self):
		return u"%s" % self.ime


class ImeStranke(models.Model):
	stranka = models.ForeignKey(Stranka)
	ime = models.CharField(max_length=128)
	od = models.DateField(null=True)
	do = models.DateField(null=True, default=END_OF_TIME)

	class Meta:
		ordering = [ '-od']
		verbose_name_plural = u'Imena strank'


class Mandat(models.Model):
	st = models.IntegerField() # Kateri mandat
	od = models.DateField()
	do = models.DateField(blank=True, default=END_OF_TIME)

	class Meta:
		verbose_name_plural = u'Mandati'

	def __unicode__(self):
		return unicode(self.st)

	def display(self):
		return u"%d mandat: %s - %s" % (self.st, self.od, self.do if self.do else "")


class Skupina(models.Model): # Poslanska
	ime = models.CharField(max_length=64)
	stranka = models.ForeignKey(Stranka, null=True, blank=True)
	od = models.DateField(null=True, blank=True)
	do = models.DateField(null=True, blank=True)
	mandat = models.ForeignKey(Mandat)
	organizacija = models.OneToOneField(Organizacija, null=True)

	def save(self, *args, **kwargs):
		if not self.organizacija_id:
			self.organizacija = Organizacija.objects.create()
		super(Skupina, self).save(*args, **kwargs)

	class Meta:
		verbose_name_plural = u'Skupine'

	def display(self):
		return ""

class DrzavniZbor(models.Model):
	mandat = models.ForeignKey(Mandat)
	organizacija = models.OneToOneField(Organizacija, null=True)

	def save(self, *args, **kwargs):
		if not self.organizacija_id:
			self.organizacija = Organizacija.objects.create()
		super(DrzavniZbor, self).save(*args, **kwargs)

	class Meta:
		verbose_name = u'Državni Zbor'
		verbose_name_plural = u'Državni Zbori'

	def display(self):
		return u"%d. mandat Državnega zbora" % self.mandat.st


class DelovnoTelo(models.Model):
	ime = models.CharField(max_length=2000)
	dz_id = models.CharField(max_length=10)
	mandat = models.ForeignKey(Mandat)
	url = models.URLField(blank=True, default="")
	od = models.DateField()
	do = models.DateField(blank=True)
	podatki_preverjeni = models.BooleanField(default=False)
	opombe = models.TextField(blank=True)
	organizacija = models.OneToOneField(Organizacija, null=True)

	def save(self, *args, **kwargs):
		if not self.organizacija_id:
			self.organizacija = Organizacija.objects.create()
		super(DelovnoTelo, self).save(*args, **kwargs)

	class Meta:
		verbose_name = u'Delovno telo'
		verbose_name_plural = u'Delovna telesa'

	def __unicode__(self):
		return '%s (%s)' % (self.ime, self.mandat)

	def display(self):
		return u"%s" % self.ime

class Pozicija(models.Model):
	oseba = models.ForeignKey(Oseba)
	organizacija = models.ForeignKey(Organizacija, null=True)
	tip = models.CharField(max_length=64, default='poslanec', choices=FUNKCIJE)
	od = models.DateField()
	do = models.DateField(blank=True, default=END_OF_TIME)
	podatki_preverjeni = models.BooleanField(default=False)
	opombe = models.TextField(blank=True)

	class Meta:
		verbose_name = u'Pozicija'
		verbose_name_plural = u'Pozicije'

	def trajanje(self):
		od = self.od.strftime("%d.%m.%Y")
		do = self.do.strftime("%d.%m.%Y") if self.do != END_OF_TIME else ""
		return u"%s - %s" % (od, do)
