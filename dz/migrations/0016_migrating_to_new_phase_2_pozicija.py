# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Pozicija'
        db.create_table('dz_pozicija', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('oseba', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dz.Oseba'])),
            ('tip_organizacije', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('id_organizacije', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('tip', self.gf('django.db.models.fields.CharField')(default='poslanec', max_length=64)),
            ('od', self.gf('django.db.models.fields.DateField')()),
            ('do', self.gf('django.db.models.fields.DateField')(blank=True)),
            ('podatki_preverjeni', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('opombe', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('dz', ['Pozicija'])


    def backwards(self, orm):
        
        # Deleting model 'Pozicija'
        db.delete_table('dz_pozicija')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'dz.clanodbora': {
            'Meta': {'object_name': 'ClanOdbora'},
            'do': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'funkcija': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mandat': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dz.Mandat']"}),
            'od': ('django.db.models.fields.DateField', [], {}),
            'odbor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dz.Odbor']"}),
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
        'dz.drzavnizbor': {
            'Meta': {'object_name': 'DrzavniZbor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mandat': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dz.Mandat']"})
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
        'dz.odbor': {
            'Meta': {'object_name': 'Odbor'},
            'do': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ime': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'mandat': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dz.Mandat']"}),
            'od': ('django.db.models.fields.DateField', [], {}),
            'opombe': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'podatki_preverjeni': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'url': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200', 'blank': 'True'})
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
            'do': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_organizacije': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'od': ('django.db.models.fields.DateField', [], {}),
            'opombe': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'oseba': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dz.Oseba']"}),
            'podatki_preverjeni': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tip': ('django.db.models.fields.CharField', [], {'default': "'poslanec'", 'max_length': '64'}),
            'tip_organizacije': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"})
        },
        'dz.skupina': {
            'Meta': {'object_name': 'Skupina'},
            'do': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ime': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'mandat': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dz.Mandat']"}),
            'od': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'stranka': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dz.Stranka']", 'null': 'True', 'blank': 'True'})
        },
        'dz.stranka': {
            'Meta': {'object_name': 'Stranka'},
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
            'podatki_preverjeni': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'spletna_stran': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'twitter': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'})
        }
    }

    complete_apps = ['dz']
