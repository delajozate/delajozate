from django.db import models
from delajozate.dz.models import Oseba

class Seja(models.Model):
    naslov = models.CharField(max_length=255)
    seja = models.CharField(max_length=255) # TODO: check validity
    slug = models.CharField(max_length=100, db_index=True)
    status = models.CharField(max_length=128)
    mandat = models.IntegerField()
    url = models.URLField()

    class Meta:
        #ordering = ('datum_zacetka',) # XXX FIXME
        pass

    def __unicode__(self):
        return self.naslov

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