from django.db import models
from django.template.defaultfilters import slugify

class Oseba(models.Model):
	ime = models.CharField(max_length=32)
	priimek = models.CharField(max_length=64)
	slug = models.SlugField(max_length=96)
	email = models.EmailField(max_length=64, blank=True)
	rojstni_dan = models.DateField(blank=True, null=True)
	slika = models.URLField(blank=True)
	spletna_stran = models.URLField(blank=True)
	twitter = models.CharField(max_length=32, blank=True)
	facebook = models.URLField(blank=True)

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slug = slugify("%s %s" % (self.ime, self.priimek))
			count = 2
			while Oseba.objects.filter(slug=self.slug).count():
				self.slug = "%s-%d" % (slug, count)
				count += 1
				
		super(Oseba, self).save(*args, **kwargs)


class Stranka(models.Model):
	ime = models.CharField(max_length=64)
	okrajsava = models.CharField(max_length=8)
	email = models.EmailField(max_length=64)
	barva = models.CharField(max_length=6)
	od = models.DateField()
	do = models.DateField(blank=True, null=True)
	spletna_stran = models.URLField(blank=True)
	twitter = models.CharField(max_length=32, blank=True)
	facebook = models.URLField(blank=True)


class Skupina(models.Model): # Poslanska
	ime = models.CharField(max_length=64)
	stranka = models.ForeignKey(Stranka, null=True, blank=True)


class ClanStranke(models.Model):
	oseba = models.ForeignKey(Oseba)
	od = models.DateField()
	do = models.DateField(blank=True)


class Mandat(models.Model):
	st = models.IntegerField() # Kateri mandat
	od = models.DateField()
	do = models.DateField(blank=True)


class Poslanec(models.Model):
	oseba = models.ForeignKey(Oseba)
	mandat = models.ForeignKey(Mandat)
	od = models.DateField()
	do = models.DateField(blank=True)


class Odbor(models.Model):
	ime = models.CharField(max_length=64)
	mandat = models.ForeignKey(Mandat)
	od = models.DateField()
	do = models.DateField(blank=True)


class ClanOdbora(models.Model):
	odbor = models.ForeignKey(Odbor)
	poslanec = models.ForeignKey(Poslanec)
	mandat = models.ForeignKey(Mandat)
	funkcija = models.CharField(max_length=32)
	od = models.DateField()
	do = models.DateField(blank=True)
