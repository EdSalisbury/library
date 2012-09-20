# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Amazon'
        db.create_table('vendor_amazon', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('access_key', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('secret_key', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('assoc_tag', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('vendor', ['Amazon'])


    def backwards(self, orm):
        # Deleting model 'Amazon'
        db.delete_table('vendor_amazon')


    models = {
        'vendor.amazon': {
            'Meta': {'object_name': 'Amazon'},
            'access_key': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'assoc_tag': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'secret_key': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        }
    }

    complete_apps = ['vendor']