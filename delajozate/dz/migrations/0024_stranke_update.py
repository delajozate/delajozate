# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):
	
	STRANKE_MAP = {
		1: 2,
		34: 6,
		33: 6,
		37: 8,
		35: 10,
		36: 10,
		7: 10,
		9: 10,
		12: 14,
		26: 14,
		15: 17,
		16: 17,
		27: 17,
		20: 21,
		24: 23,
		40: 39,
		42: 43,
	}
	
	def forwards(self, orm):
		"""
		1. Vsaka Stranka dobi ImeStranke z ustreznim časom
		2. Vsaka Pozicija vezana na Stranka, ki ima po novem nov ID se spremeni na nov ID
		3. Pozicije, ki so zaporedne po datumih za isto stranko se združijo
		"""
		# Step 1
		for s in orm.Stranka.objects.all():
			nid = self.STRANKE_MAP.get(s.id, s.id) # id je nov če obstaja oz. isti če ne
			stranka = orm.Stranka.objects.get(pk=nid)
			orm.ImeStranke.objects.create(**{
				"stranka": stranka,
				"ime": s.ime,
				"od": s.od,
				"do": s.do
			})
		
		# Step 2
		for p in orm.Pozicija.objects.filter(organizacija__stranka__in=self.STRANKE_MAP.keys()):
			nid = self.STRANKE_MAP.get(s.id, s.id) # id je nov če obstaja oz. isti če ne
			p.organizacija = orm.Organizacija.objects.get(stranka__id=nid)
			p.save()
		
		# Step 3
		merge_these = []
		def pozicije_join(pozicije):
			if len(pozicije) > 1:
				fp = pozicije.pop(0)
				fp.do = pozicije[-1].do
				fp.save()
				for p in pozicije:
					p.delete()
			
		for p in orm.Pozicija.objects.filter(organizacija__stranka__gt=0).order_by("oseba__id", "od"):
			if not len(merge_these):
				merge_these.append(p)
			else:
				lp = merge_these[-1]
				if lp.oseba == p.oseba and lp.do == p.od and lp.organizacija == p.organizacija:
					merge_these.append(p)
				else:
					# process previous data
					pozicije_join(merge_these)
					# start new set
					merge_these = [p]
				
	
	
	def backwards(self, orm):
		"Write your backwards methods here."
		raise RuntimeError("Cannot reverse this migration.")
	
	
	models = {
		'dz.clanodbora': {
			'Meta': {'object_name': 'ClanOdbora'},
			'do': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
			'funkcija': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
			'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'mandat': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dz.Mandat']"}),
			'od': ('django.db.models.fields.DateField', [], {}),
			'odbor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dz.DelovnoTelo']"}),
			'opombe': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
			'podatki_preverjeni': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
			'poslanec': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dz.Funkcija']"})
		},
		'dz.clanstranke': {
			'Meta': {'ordering': "('-do',)", 'object_name': 'ClanStranke'},
			'do': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
			'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'od': ('django.db.models.fields.DateField', [], {}),
			'opombe': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
			'oseba': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dz.Oseba']"}),
			'podatki_preverjeni': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
			'stranka': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dz.Stranka']", 'null': 'True', 'blank': 'True'})
		},
		'dz.delovnotelo': {
			'Meta': {'object_name': 'DelovnoTelo'},
			'do': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
			'dz_id': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
			'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'ime': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
			'mandat': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dz.Mandat']"}),
			'od': ('django.db.models.fields.DateField', [], {}),
			'opombe': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
			'organizacija': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['dz.Organizacija']", 'unique': 'True', 'null': 'True'}),
			'podatki_preverjeni': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
			'url': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200', 'blank': 'True'})
		},
		'dz.drzavnizbor': {
			'Meta': {'object_name': 'DrzavniZbor'},
			'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'mandat': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dz.Mandat']"}),
			'organizacija': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['dz.Organizacija']", 'unique': 'True', 'null': 'True'})
		},
		'dz.funkcija': {
			'Meta': {'ordering': "('id',)", 'object_name': 'Funkcija'},
			'do': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
			'funkcija': ('django.db.models.fields.CharField', [], {'default': "'poslanec'", 'max_length': '64'}),
			'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'mandat': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dz.Mandat']"}),
			'od': ('django.db.models.fields.DateField', [], {}),
			'opombe': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
			'oseba': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dz.Oseba']"}),
			'podatki_preverjeni': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
		},
		'dz.imestranke': {
			'Meta': {'ordering': "['-od']", 'object_name': 'ImeStranke'},
			'do': ('django.db.models.fields.DateField', [], {'default': 'datetime.date(9999, 12, 31)', 'null': 'True'}),
			'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'ime': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
			'od': ('django.db.models.fields.DateField', [], {'null': 'True'}),
			'stranka': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dz.Stranka']"})
		},
		'dz.mandat': {
			'Meta': {'object_name': 'Mandat'},
			'do': ('django.db.models.fields.DateField', [], {'default': 'datetime.date(9999, 12, 31)', 'blank': 'True'}),
			'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'od': ('django.db.models.fields.DateField', [], {}),
			'st': ('django.db.models.fields.IntegerField', [], {})
		},
		'dz.organizacija': {
			'Meta': {'object_name': 'Organizacija'},
			'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
		},
		'dz.oseba': {
			'Meta': {'ordering': "('ime', 'priimek')", 'object_name': 'Oseba'},
			'dan_smrti': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
			'email': ('django.db.models.fields.EmailField', [], {'max_length': '64', 'blank': 'True'}),
			'facebook': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
			'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'ime': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
			'opombe': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
			'podatki_preverjeni': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
			'priimek': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
			'rojstni_dan': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
			'slika': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
			'slug': ('django.db.models.fields.SlugField', [], {'max_length': '96', 'db_index': 'True'}),
			'spletna_stran': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
			'twitter': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
			'vir_slike': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
		},
		'dz.pozicija': {
			'Meta': {'object_name': 'Pozicija'},
			'do': ('django.db.models.fields.DateField', [], {'default': 'datetime.date(9999, 12, 31)', 'blank': 'True'}),
			'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'od': ('django.db.models.fields.DateField', [], {}),
			'opombe': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
			'organizacija': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dz.Organizacija']", 'null': 'True'}),
			'oseba': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dz.Oseba']"}),
			'podatki_preverjeni': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
			'tip': ('django.db.models.fields.CharField', [], {'default': "'poslanec'", 'max_length': '64'})
		},
		'dz.skupina': {
			'Meta': {'object_name': 'Skupina'},
			'do': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
			'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'ime': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
			'mandat': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dz.Mandat']"}),
			'od': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
			'organizacija': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['dz.Organizacija']", 'unique': 'True', 'null': 'True'}),
			'stranka': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dz.Stranka']", 'null': 'True', 'blank': 'True'})
		},
		'dz.stranka': {
			'Meta': {'ordering': "('-do', 'ime')", 'object_name': 'Stranka'},
			'barva': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
			'davcna': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
			'do': ('django.db.models.fields.DateField', [], {'default': 'datetime.date(9999, 12, 31)', 'null': 'True'}),
			'email': ('django.db.models.fields.EmailField', [], {'max_length': '64', 'blank': 'True'}),
			'facebook': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
			'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'ime': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
			'maticna': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
			'nastala_iz': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'spremenila_v'", 'blank': 'True', 'to': "orm['dz.Stranka']"}),
			'od': ('django.db.models.fields.DateField', [], {'null': 'True'}),
			'okrajsava': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
			'opombe': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
			'organizacija': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['dz.Organizacija']", 'unique': 'True', 'null': 'True'}),
			'podatki_preverjeni': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
			'spletna_stran': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
			'twitter': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'})
		}
	}

	complete_apps = ['dz']
