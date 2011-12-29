# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'Povezava'
        db.delete_table('search_povezava')

        # Adding model 'Zapis'
        db.create_table('search_zapis', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('zasedanje', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['iskanje.Zasedanje'])),
            ('odstavki', self.gf('django.db.models.fields.TextField')(null=True)),
            ('govorec', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
        ))
        db.send_create_signal('search', ['Zapis'])

        # Adding field 'Zasedanje.naslov'
        db.add_column('search_zasedanje', 'naslov', self.gf('django.db.models.fields.CharField')(max_length=255, null=True), keep_default=False)

        # Adding field 'Zasedanje.zacetek'
        db.add_column('search_zasedanje', 'zacetek', self.gf('django.db.models.fields.TimeField')(null=True), keep_default=False)

        # Adding field 'Zasedanje.konec'
        db.add_column('search_zasedanje', 'konec', self.gf('django.db.models.fields.TimeField')(null=True), keep_default=False)

        # Adding field 'Zasedanje.url'
        db.add_column('search_zasedanje', 'url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True), keep_default=False)

        # Adding field 'Zasedanje.tip'
        db.add_column('search_zasedanje', 'tip', self.gf('django.db.models.fields.CharField')(max_length=255, null=True), keep_default=False)

        # Changing field 'Zasedanje.datum'
        db.alter_column('search_zasedanje', 'datum', self.gf('django.db.models.fields.DateField')(null=True))


    def backwards(self, orm):
        
        # Adding model 'Povezava'
        db.create_table('search_povezava', (
            ('zasedanje', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['iskanje.Zasedanje'])),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('tip', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('naslov', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('search', ['Povezava'])

        # Deleting model 'Zapis'
        db.delete_table('search_zapis')

        # Deleting field 'Zasedanje.naslov'
        db.delete_column('search_zasedanje', 'naslov')

        # Deleting field 'Zasedanje.zacetek'
        db.delete_column('search_zasedanje', 'zacetek')

        # Deleting field 'Zasedanje.konec'
        db.delete_column('search_zasedanje', 'konec')

        # Deleting field 'Zasedanje.url'
        db.delete_column('search_zasedanje', 'url')

        # Deleting field 'Zasedanje.tip'
        db.delete_column('search_zasedanje', 'tip')

        # Changing field 'Zasedanje.datum'
        db.alter_column('search_zasedanje', 'datum', self.gf('django.db.models.fields.DateField')(default=datetime.date(2011, 9, 30)))


    models = {
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
        'search.zapis': {
            'Meta': {'object_name': 'Zapis'},
            'govorec': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'odstavki': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'zasedanje': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['search.Zasedanje']"})
        },
        'search.zasedanje': {
            'Meta': {'object_name': 'Zasedanje'},
            'datum': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'konec': ('django.db.models.fields.TimeField', [], {'null': 'True'}),
            'naslov': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'seja': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['search.Seja']"}),
            'tip': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'zacetek': ('django.db.models.fields.TimeField', [], {'null': 'True'})
        }
    }

    complete_apps = ['search']
