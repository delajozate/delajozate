# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Event.title'
        db.alter_column('cal_event', 'title', self.gf('django.db.models.fields.CharField')(max_length=2000))

        # Changing field 'Event.url'
        db.alter_column('cal_event', 'url', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True))


    def backwards(self, orm):
        
        # Changing field 'Event.title'
        db.alter_column('cal_event', 'title', self.gf('django.db.models.fields.CharField')(max_length=500))

        # Changing field 'Event.url'
        db.alter_column('cal_event', 'url', self.gf('django.db.models.fields.CharField')(default='', max_length=1000))


    models = {
        'cal.event': {
            'Meta': {'object_name': 'Event'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'vir': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['cal']
