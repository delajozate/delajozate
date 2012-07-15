# coding: utf-8
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
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
	

class Organizacija(models.Model):
	def type(self, value=False):
		for p in ["stranka", "skupina", "drzavnizbor", "odbor"]:
			try:
				v = getattr(self, p)
				return v if value else p
			except ObjectDoesNotExist:
				pass
		return None if value else "unknown" 
	
	def __unicode__(self):
		t = self.type()
		return u"[%s] %s" % (t, getattr(self, t)) if t != "unknown" else None
	
	def value(self):
		return self.type(True)
	

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
		ordering = ('ime', 'priimek')
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
	
	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slug = slugify("%s %s" % (self.ime, self.priimek))
			count = 2
			while Oseba.objects.filter(slug=self.slug).count():
				self.slug = "%s-%d" % (slug, count)
				count += 1
		super(Oseba, self).save(*args, **kwargs)
	

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
	
	def __unicode__(self):
		return u'%s (%s)%s' % (self.ime, self.okrajsava, self.do != END_OF_TIME and u'\u271d' or u'')
	

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
	

class Odbor(models.Model):
	ime = models.CharField(max_length=500)
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
		super(Odbor, self).save(*args, **kwargs)
	
	class Meta:
		verbose_name_plural = u'Odbori'
	
	def __unicode__(self):
		return '%s (%s)' % (self.ime, self.mandat)
	

class Funkcija(models.Model):
	oseba = models.ForeignKey(Oseba)
	funkcija = models.CharField(max_length=64, default='poslanec', choices=FUNKCIJE)
	mandat = models.ForeignKey(Mandat)
	od = models.DateField()
	do = models.DateField(blank=True)
	podatki_preverjeni = models.BooleanField(default=False)
	opombe = models.TextField(blank=True)
	
	class Meta:
		ordering = ('id',)
		verbose_name_plural = u'Funkcije'
	
	def __unicode__(self):
		return u'%s (%s)' % (self.oseba, self.mandat)
	

class ClanStranke(models.Model):
	oseba = models.ForeignKey(Oseba)
	stranka = models.ForeignKey(Stranka, null=True, blank=True)
	od = models.DateField()
	do = models.DateField(blank=True)
	podatki_preverjeni = models.BooleanField(default=False)
	opombe = models.TextField(blank=True)
	
	class Meta:
		verbose_name = u'Član stranke'
		verbose_name_plural = u'Člani strank'
		ordering = ('-do',)
	

class ClanOdbora(models.Model):
	odbor = models.ForeignKey(Odbor)
	poslanec = models.ForeignKey(Funkcija)
	mandat = models.ForeignKey(Mandat)
	funkcija = models.CharField(max_length=32)
	od = models.DateField()
	do = models.DateField(blank=True)
	podatki_preverjeni = models.BooleanField(default=False)
	opombe = models.TextField(blank=True)
	
	class Meta:
		verbose_name = u'Član odbora'
		verbose_name_plural = u'Člani odbora'
	

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
	
