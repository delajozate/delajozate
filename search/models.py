from django.db import models

# Modeli za magnetograme
class Seja(models.Model):
    naslov = models.CharField()
    seja = models.CharField() # TODO: check validity
    status = models.CharField()
    mandat = models.IntegerField()
    url = models.URLField()

class SejaInfo(models.Model):
    seja = models.ForeignKey(Seja)
    url = models.URLField()
    naslov = models.CharField()
    datum = models.DateField()

class Zasedanje(models.Model):
    seja = models.ForeignKey(Seja)
    datum = models.DateField()

class Povezava(models.Model):
    zasedanje = models.ForeignKey(Povezava)
    url = models.URLField()
    text = models.TextField()
    naslov = models.CharField()
    tip = models.CharField()