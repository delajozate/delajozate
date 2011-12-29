# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Seja'
        db.create_table('search_seja', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('naslov', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('seja', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('mandat', self.gf('django.db.models.fields.IntegerField')()),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('search', ['Seja'])

        # Adding model 'SejaInfo'
        db.create_table('search_sejainfo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('seja', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['iskanje.Seja'])),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('naslov', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('datum', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('search', ['SejaInfo'])

        # Adding model 'Zasedanje'
        db.create_table('search_zasedanje', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('seja', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['iskanje.Seja'])),
            ('datum', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('search', ['Zasedanje'])

        # Adding model 'Povezava'
        db.create_table('search_povezava', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('zasedanje', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['iskanje.Zasedanje'])),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('naslov', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('tip', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('search', ['Povezava'])


    def backwards(self, orm):
        
        # Deleting model 'Seja'
        db.delete_table('search_seja')

        # Deleting model 'SejaInfo'
        db.delete_table('search_sejainfo')

        # Deleting model 'Zasedanje'
        db.delete_table('search_zasedanje')

        # Deleting model 'Povezava'
        db.delete_table('search_povezava')


    models = {
        'search.povezava': {
            'Meta': {'object_name': 'Povezava'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'naslov': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'tip': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'zasedanje': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['search.Zasedanje']"})
        },
        'search.seja': {
            'Meta': {'object_name': 'Seja'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mandat': ('django.db.models.fields.IntegerField', [], {}),
            'naslov': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'seja': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'search.sejainfo': {
            'Meta': {'object_name': 'SejaInfo'},
            'datum': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'naslov': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'seja': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['search.Seja']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'search.zasedanje': {
            'Meta': {'object_name': 'Zasedanje'},
            'datum': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'seja': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['search.Seja']"})
        }
    }

    complete_apps = ['search']
