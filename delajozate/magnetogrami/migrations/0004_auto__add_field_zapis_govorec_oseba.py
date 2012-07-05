# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Zapis.govorec_oseba'
        db.add_column('magnetogrami_zapis', 'govorec_oseba', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dz.Oseba'], null=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Zapis.govorec_oseba'
        db.delete_column('magnetogrami_zapis', 'govorec_oseba_id')


    models = {
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
            'twitter': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'})
        },
        'magnetogrami.seja': {
            'Meta': {'object_name': 'Seja'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mandat': ('django.db.models.fields.IntegerField', [], {}),
            'naslov': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'seja': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
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
            'Meta': {'ordering': "('seq',)", 'object_name': 'Zapis'},
            'govorec': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'govorec_oseba': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dz.Oseba']", 'null': 'True'}),
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
