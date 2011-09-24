from django.db import models

# Modeli za magnetograme
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
    datum = models.DateField()

class Povezava(models.Model):
    zasedanje = models.ForeignKey(Zasedanje)
    url = models.URLField()
    text = models.TextField()
    naslov = models.CharField(max_length=255)
    tip = models.CharField(max_length=255)