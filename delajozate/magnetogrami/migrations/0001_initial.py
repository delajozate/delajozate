# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Seja'
        db.create_table('magnetogrami_seja', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('naslov', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('seja', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('mandat', self.gf('django.db.models.fields.IntegerField')()),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('magnetogrami', ['Seja'])

        # Adding model 'SejaInfo'
        db.create_table('magnetogrami_sejainfo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('seja', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['magnetogrami.Seja'])),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('naslov', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('datum', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('magnetogrami', ['SejaInfo'])

        # Adding model 'Zasedanje'
        db.create_table('magnetogrami_zasedanje', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('seja', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['magnetogrami.Seja'])),
            ('naslov', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('datum', self.gf('django.db.models.fields.DateField')(null=True)),
            ('zacetek', self.gf('django.db.models.fields.TimeField')(null=True)),
            ('konec', self.gf('django.db.models.fields.TimeField')(null=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True)),
            ('tip', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
        ))
        db.send_create_signal('magnetogrami', ['Zasedanje'])

        # Adding model 'Zapis'
        db.create_table('magnetogrami_zapis', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('zasedanje', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['magnetogrami.Zasedanje'])),
            ('odstavki', self.gf('django.db.models.fields.TextField')(null=True)),
            ('govorec', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
        ))
        db.send_create_signal('magnetogrami', ['Zapis'])


    def backwards(self, orm):
        
        # Deleting model 'Seja'
        db.delete_table('magnetogrami_seja')

        # Deleting model 'SejaInfo'
        db.delete_table('magnetogrami_sejainfo')

        # Deleting model 'Zasedanje'
        db.delete_table('magnetogrami_zasedanje')

        # Deleting model 'Zapis'
        db.delete_table('magnetogrami_zapis')


    models = {
        'magnetogrami.seja': {
            'Meta': {'object_name': 'Seja'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mandat': ('django.db.models.fields.IntegerField', [], {}),
            'naslov': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'seja': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'magnetogrami.sejainfo': {
            'Meta': {'object_name': 'SejaInfo'},
            'datum': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'naslov': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'seja': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['magnetogrami.Seja']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'magnetogrami.zapis': {
            'Meta': {'object_name': 'Zapis'},
            'govorec': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'odstavki': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'zasedanje': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['magnetogrami.Zasedanje']"})
        },
        'magnetogrami.zasedanje': {
            'Meta': {'object_name': 'Zasedanje'},
            'datum': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'konec': ('django.db.models.fields.TimeField', [], {'null': 'True'}),
            'naslov': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'seja': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['magnetogrami.Seja']"}),
            'tip': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'zacetek': ('django.db.models.fields.TimeField', [], {'null': 'True'})
        }
    }

    complete_apps = ['magnetogrami']
