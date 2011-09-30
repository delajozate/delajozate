from django.db import models

# Modeli za magnetograme
from haystack.fields import CharField
from haystack.indexes import SearchIndex
from haystack.sites import site

class Seja(models.Model):
    naslov = models.CharField(max_length=255)
    seja = models.CharField(max_length=255) # TODO: check validity
    status = models.CharField(max_length=128)
    mandat = models.IntegerField()
    url = models.URLField()

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

class Zapis(models.Model):
    zasedanje = models.ForeignKey(Zasedanje)
    odstavki = models.TextField(null=True)
    govorec = models.CharField(max_length=255, null=True)