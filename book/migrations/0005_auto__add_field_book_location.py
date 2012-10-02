# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Book.location'
        db.add_column('book_book', 'location',
                      self.gf('django.db.models.fields.CharField')(default='unknown', max_length=16),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Book.location'
        db.delete_column('book_book', 'location')


    models = {
        'book.author': {
            'Meta': {'object_name': 'Author'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'book.book': {
            'Meta': {'object_name': 'Book'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['book.Author']"}),
            'condition': ('django.db.models.fields.related.ForeignKey', [], {'default': '7', 'to': "orm['book.Condition']"}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'format': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['book.Format']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isbn': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '15'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'publication_year': ('django.db.models.fields.IntegerField', [], {}),
            'publisher': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['book.Publisher']"}),
            'series': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['book.Series']", 'null': 'True', 'blank': 'True'}),
            'series_number': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'book.condition': {
            'Meta': {'object_name': 'Condition'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        'book.format': {
            'Meta': {'object_name': 'Format'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'book.publisher': {
            'Meta': {'object_name': 'Publisher'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'book.series': {
            'Meta': {'object_name': 'Series'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['book']