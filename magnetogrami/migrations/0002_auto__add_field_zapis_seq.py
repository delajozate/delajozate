# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Zapis.seq'
        db.add_column('magnetogrami_zapis', 'seq', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Zapis.seq'
        db.delete_column('magnetogrami_zapis', 'seq')


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
            'seq': ('django.db.models.fields.IntegerField', [], {}),
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
