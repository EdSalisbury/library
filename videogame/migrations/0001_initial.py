# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Developer'
        db.create_table('videogame_developer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('videogame', ['Developer'])

        # Adding model 'Condition'
        db.create_table('videogame_condition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=16)),
        ))
        db.send_create_signal('videogame', ['Condition'])

        # Adding model 'MediaType'
        db.create_table('videogame_mediatype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('videogame', ['MediaType'])

        # Adding model 'Publisher'
        db.create_table('videogame_publisher', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('videogame', ['Publisher'])

        # Adding model 'Series'
        db.create_table('videogame_series', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('videogame', ['Series'])

        # Adding model 'VideoGame'
        db.create_table('videogame_videogame', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('developer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['videogame.Developer'])),
            ('condition', self.gf('django.db.models.fields.related.ForeignKey')(default=7, to=orm['videogame.Condition'])),
            ('media_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['videogame.MediaType'])),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('publisher', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['videogame.Publisher'])),
            ('series', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['videogame.Series'], null=True, blank=True)),
            ('series_number', self.gf('django.db.models.fields.CharField')(max_length=5, blank=True)),
            ('publication_year', self.gf('django.db.models.fields.IntegerField')()),
            ('isbn', self.gf('django.db.models.fields.CharField')(default='', max_length=15)),
            ('description', self.gf('django.db.models.fields.TextField')(default='')),
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('updated_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal('videogame', ['VideoGame'])


    def backwards(self, orm):
        # Deleting model 'Developer'
        db.delete_table('videogame_developer')

        # Deleting model 'Condition'
        db.delete_table('videogame_condition')

        # Deleting model 'MediaType'
        db.delete_table('videogame_mediatype')

        # Deleting model 'Publisher'
        db.delete_table('videogame_publisher')

        # Deleting model 'Series'
        db.delete_table('videogame_series')

        # Deleting model 'VideoGame'
        db.delete_table('videogame_videogame')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'videogame.condition': {
            'Meta': {'object_name': 'Condition'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        'videogame.developer': {
            'Meta': {'object_name': 'Developer'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'videogame.mediatype': {
            'Meta': {'object_name': 'MediaType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'videogame.publisher': {
            'Meta': {'object_name': 'Publisher'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'videogame.series': {
            'Meta': {'object_name': 'Series'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'videogame.videogame': {
            'Meta': {'ordering': "['developer__name', 'publication_year', 'title']", 'object_name': 'VideoGame'},
            'condition': ('django.db.models.fields.related.ForeignKey', [], {'default': '7', 'to': "orm['videogame.Condition']"}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'developer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['videogame.Developer']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isbn': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '15'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'media_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['videogame.MediaType']"}),
            'publication_year': ('django.db.models.fields.IntegerField', [], {}),
            'publisher': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['videogame.Publisher']"}),
            'series': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['videogame.Series']", 'null': 'True', 'blank': 'True'}),
            'series_number': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'updated_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        }
    }

    complete_apps = ['videogame']