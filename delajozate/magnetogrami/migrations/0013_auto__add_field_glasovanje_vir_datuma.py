# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Glasovanje.vir_datuma'
        db.add_column('magnetogrami_glasovanje', 'vir_datuma', self.gf('django.db.models.fields.CharField')(default='', max_length=20), keep_default=False)
        
        for g in orm.Glasovanje.objects.all():
            if g.datum is not None:
                g.vir_datuma = 'original'
            else:
                zasedanja = list(g.seja.zasedanje_set.all().order_by('-datum'))
                if len(zasedanja) > 0:
                    g.datum = zasedanja[0].datum
                    g.vir_datuma = 'zadnje zasedanje'
                    g.save()

    def backwards(self, orm):
        
        # Deleting field 'Glasovanje.vir_datuma'
        db.delete_column('magnetogrami_glasovanje', 'vir_datuma')


    models = {
        'dz.oseba': {
            'Meta': {'ordering': "('priimek', 'ime')", 'object_name': 'Oseba'},
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
        'magnetogrami.glas': {
            'Meta': {'ordering': "('oseba__priimek', 'oseba__ime')", 'object_name': 'Glas'},
            'glasoval': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'glasovanje': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['magnetogrami.Glasovanje']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kvorum': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'oseba': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dz.Oseba']", 'null': 'True'}),
            'poslanec': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'magnetogrami.glasovanje': {
            'Meta': {'ordering': "('-seja__mandat', '-datum')", 'object_name': 'Glasovanje'},
            'datum': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'dokument': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True'}),
            'faza_postopka': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'naslov': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True'}),
            'seja': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['magnetogrami.Seja']", 'null': 'True'}),
            'ura': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'vir_datuma': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20'}),
            'zapis': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['magnetogrami.Zapis']", 'null': 'True'})
        },
        'magnetogrami.govorecmap': {
            'Meta': {'object_name': 'GovorecMap'},
            'govorec': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'oseba': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dz.Oseba']"})
        },
        'magnetogrami.seja': {
            'Meta': {'ordering': "('-mandat', '-datum_zacetka')", 'object_name': 'Seja'},
            'datum_zacetka': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'delovno_telo': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mandat': ('django.db.models.fields.IntegerField', [], {}),
            'naslov': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'seja': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
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
            'Meta': {'ordering': "('datum',)", 'object_name': 'Zasedanje'},
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
