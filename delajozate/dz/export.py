import inspect

from django.conf import settings
from django.core.serializers import serialize
from django.db import models

# need to do it this way so the command works. beats me why...
import django.contrib.staticfiles.models as staticfilesModels
import django.contrib.auth.models as authModels
import django.contrib.sites.models as siteModels
import django.contrib.admin.models as adminModels
import django.contrib.contenttypes.models as contenttypeModels
import django.contrib.sessions.models as sessionModels
import south.models as southModels
import delajozate.dz.models as dzModels
import delajozate.magnetogrami.models as magnetogramiModels

# Make sure to use the correct order so dependencies are not broken

MODELS = (
	siteModels.Site,
	authModels.Group,
	authModels.User,
	dzModels.Organizacija,
	dzModels.Oseba,
	dzModels.Stranka, # Organizacija
	dzModels.ImeStranke, # Stranka
	dzModels.Mandat, 
	dzModels.Skupina, # Stranka, Organizacija
	dzModels.DrzavniZbor, # Mandat, Organizacija
	dzModels.Odbor, # Mandat, Organizacija
	dzModels.Funkcija, # Oseba, Mandat
 	#dzModels.ClanStranke, # Oseba, Stranka
	dzModels.ClanOdbora, # Odbor, Funkcija, Mandat
	dzModels.Pozicija, # Oseba, Organizacija
	magnetogramiModels.GovorecMap,
)

IGNORE_MODELS = (
	authModels.Permission,
	authModels.Message,
	adminModels.LogEntry,
	southModels.MigrationHistory,
	contenttypeModels.ContentType,
	sessionModels.Session,
	magnetogramiModels.Seja, 
	magnetogramiModels.SejaInfo, # Seja
	magnetogramiModels.Zasedanje, # Seja
	magnetogramiModels.Zapis, # Zasedanje
)

def get_class(class_str):
	parts = class_str.split('.')
	root = parts.pop(0)
	app = __import__(root)
	while parts:
		try:
			app = getattr(app, parts.pop(0))
		except AttributeError:
			print "Cannot import models for %s - possibly some models will not be exported." % class_str
	return app
	

def get_model_classes(verbose=False):
	list = set([])
	for appstring in settings.INSTALLED_APPS:
		app = get_class(appstring)
		if verbose:
			print "%s:" % appstring
		if 'models' in dir(app):
			app_models = app.models
			for prop in dir(app_models):
				model = getattr(app_models, prop)
				if inspect.isclass(model) and issubclass(model, models.Model):
					if model._meta.abstract:
						continue
					if verbose:
						print " - %s" % prop
					list.add(model)
	return list
	

for model in get_model_classes():
	if model not in MODELS and model not in IGNORE_MODELS:
		raise Exception("Not all models will be exported: %s missing." % model)
	

# use exportdata(indent=2) to have a readable output
# all kwargs are sent to serialize and in turn to json.dump()
def exportdata(models=MODELS, **kwargs):
	filename = '%sexported_data.json' % (settings.FIXTURE_DIRS[0])
	file = open(filename, "w")
	l = []
	for model in models:
		l.extend(list(model.objects.all().order_by('pk')))
	s = serialize("json", l, **kwargs)
	file.write(s)
	file.close()
	return l
	

