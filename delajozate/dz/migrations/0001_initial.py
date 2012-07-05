# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Oseba'
        db.create_table('dz_oseba', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ime', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('priimek', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=96, db_index=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=64, blank=True)),
            ('rojstni_dan', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('slika', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('spletna_stran', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('twitter', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('facebook', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('dz', ['Oseba'])

        # Adding model 'Stranka'
        db.create_table('dz_stranka', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ime', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('okrajsava', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=64)),
            ('barva', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('od', self.gf('django.db.models.fields.DateField')()),
            ('do', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('spletna_stran', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('twitter', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('facebook', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('dz', ['Stranka'])

        # Adding model 'Skupina'
        db.create_table('dz_skupina', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ime', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('stranka', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dz.Stranka'], null=True, blank=True)),
        ))
        db.send_create_signal('dz', ['Skupina'])

        # Adding model 'ClanStranke'
        db.create_table('dz_clanstranke', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('oseba', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dz.Oseba'])),
            ('od', self.gf('django.db.models.fields.DateField')()),
            ('do', self.gf('django.db.models.fields.DateField')(blank=True)),
        ))
        db.send_create_signal('dz', ['ClanStranke'])

        # Adding model 'Mandat'
        db.create_table('dz_mandat', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('st', self.gf('django.db.models.fields.IntegerField')()),
            ('od', self.gf('django.db.models.fields.DateField')()),
            ('do', self.gf('django.db.models.fields.DateField')(blank=True)),
        ))
        db.send_create_signal('dz', ['Mandat'])

        # Adding model 'Poslanec'
        db.create_table('dz_poslanec', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('oseba', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dz.Oseba'])),
            ('mandat', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dz.Mandat'])),
            ('od', self.gf('django.db.models.fields.DateField')()),
            ('do', self.gf('django.db.models.fields.DateField')(blank=True)),
        ))
        db.send_create_signal('dz', ['Poslanec'])

        # Adding model 'Odbor'
        db.create_table('dz_odbor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ime', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('mandat', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dz.Mandat'])),
            ('od', self.gf('django.db.models.fields.DateField')()),
            ('do', self.gf('django.db.models.fields.DateField')(blank=True)),
        ))
        db.send_create_signal('dz', ['Odbor'])

        # Adding model 'ClanOdbora'
        db.create_table('dz_clanodbora', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('odbor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dz.Odbor'])),
            ('poslanec', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dz.Poslanec'])),
            ('mandat', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dz.Mandat'])),
            ('funkcija', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('od', self.gf('django.db.models.fields.DateField')()),
            ('do', self.gf('django.db.models.fields.DateField')(blank=True)),
        ))
        db.send_create_signal('dz', ['ClanOdbora'])


    def backwards(self, orm):
        
        # Deleting model 'Oseba'
        db.delete_table('dz_oseba')

        # Deleting model 'Stranka'
        db.delete_table('dz_stranka')

        # Deleting model 'Skupina'
        db.delete_table('dz_skupina')

        # Deleting model 'ClanStranke'
        db.delete_table('dz_clanstranke')

        # Deleting model 'Mandat'
        db.delete_table('dz_mandat')

        # Deleting model 'Poslanec'
        db.delete_table('dz_poslanec')

        # Deleting model 'Odbor'
        db.delete_table('dz_odbor')

        # Deleting model 'ClanOdbora'
        db.delete_table('dz_clanodbora')


    models = {
        'dz.clanodbora': {
            'Meta': {'object_name': 'ClanOdbora'},
            'do': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'funkcija': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mandat': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dz.Mandat']"}),
            'od': ('django.db.models.fields.DateField', [], {}),
            'odbor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dz.Odbor']"}),
            'poslanec': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dz.Poslanec']"})
        },
        'dz.clanstranke': {
            'Meta': {'object_name': 'ClanStranke'},
            'do': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'od': ('django.db.models.fields.DateField', [], {}),
            'oseba': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dz.Oseba']"})
        },
        'dz.mandat': {
            'Meta': {'object_name': 'Mandat'},
            'do': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'od': ('django.db.models.fields.DateField', [], {}),
            'st': ('django.db.models.fields.IntegerField', [], {})
        },
        'dz.odbor': {
            'Meta': {'object_name': 'Odbor'},
            'do': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ime': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'mandat': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dz.Mandat']"}),
            'od': ('django.db.models.fields.DateField', [], {})
        },
        'dz.oseba': {
            'Meta': {'ordering': "('priimek', 'ime')", 'object_name': 'Oseba'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '64', 'blank': 'True'}),
            'facebook': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ime': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'priimek': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'rojstni_dan': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'slika': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '96', 'db_index': 'True'}),
            'spletna_stran': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'twitter': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'})
        },
        'dz.poslanec': {
            'Meta': {'object_name': 'Poslanec'},
            'do': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mandat': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dz.Mandat']"}),
            'od': ('django.db.models.fields.DateField', [], {}),
            'oseba': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dz.Oseba']"})
        },
        'dz.skupina': {
            'Meta': {'object_name': 'Skupina'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ime': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'stranka': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dz.Stranka']", 'null': 'True', 'blank': 'True'})
        },
        'dz.stranka': {
            'Meta': {'object_name': 'Stranka'},
            'barva': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'do': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '64'}),
            'facebook': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ime': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'od': ('django.db.models.fields.DateField', [], {}),
            'okrajsava': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'spletna_stran': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'twitter': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'})
        }
    }

    complete_apps = ['dz']
