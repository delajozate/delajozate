import inspect

from django.conf import settings
from django.core.serializers import serialize
from django.db import models

import django, south, dz, search

# Make sure to use the correct order so dependencies are not broken
MODELS = (
	django.contrib.auth.models.Group,
	django.contrib.auth.models.User,
	dz.models.Oseba,
	dz.models.Stranka,
	dz.models.Mandat,
	dz.models.Skupina, # Stranka
	dz.models.ClanStranke, # Oseba, Stranka
	dz.models.Poslanec, # Oseba, Mandat
	dz.models.Odbor, # Mandat
	dz.models.ClanOdbora, # Odbor, Poslanec, Mandat
	search.models.Seja, 
	search.models.SejaInfo, # Seja
	search.models.Zasedanje, # Seja
	search.models.Zapis, # Zasedanje
)

IGNORE_MODELS = (
	django.contrib.auth.models.Permission,
	django.contrib.auth.models.Message,
	django.contrib.admin.models.LogEntry,
	south.models.MigrationHistory,
	django.contrib.contenttypes.models.ContentType,
	django.contrib.sites.models.Site,
	django.contrib.sessions.models.Session
)

def get_class(class_str):
	parts = class_str.split('.')
	root = parts.pop(0)
	app = __import__(root)
	while parts:
		app = getattr(app, parts.pop(0))
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
		l.extend(list(model.objects.all()))
	s = serialize("json", l, **kwargs)
	file.write(s)
	file.close()
	return l
	

