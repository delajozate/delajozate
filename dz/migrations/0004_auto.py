# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding M2M table for field nastala_iz on 'Stranka'
        db.create_table('dz_stranka_nastala_iz', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_stranka', models.ForeignKey(orm['dz.stranka'], null=False)),
            ('to_stranka', models.ForeignKey(orm['dz.stranka'], null=False))
        ))
        db.create_unique('dz_stranka_nastala_iz', ['from_stranka_id', 'to_stranka_id'])


    def backwards(self, orm):
        
        # Removing M2M table for field nastala_iz on 'Stranka'
        db.delete_table('dz_stranka_nastala_iz')


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
            'do': ('django.db.models.fields.DateField', [], {'default': 'datetime.date(9999, 12, 31)', 'blank': 'True'}),
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
            'Meta': {'ordering': "('ime', 'priimek')", 'object_name': 'Oseba'},
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
            'Meta': {'ordering': "('id',)", 'object_name': 'Poslanec'},
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
            'davcna': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'do': ('django.db.models.fields.DateField', [], {'default': 'datetime.date(9999, 12, 31)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '64', 'blank': 'True'}),
            'facebook': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ime': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'maticna': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'nastala_iz': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'nastala_iz_rel_+'", 'to': "orm['dz.Stranka']"}),
            'od': ('django.db.models.fields.DateField', [], {}),
            'okrajsava': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'opombe': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'spletna_stran': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'twitter': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'})
        }
    }

    complete_apps = ['dz']
