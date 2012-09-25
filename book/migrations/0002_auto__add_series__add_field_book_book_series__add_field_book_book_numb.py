# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Series'
        db.create_table('book_series', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('book', ['Series'])

        # Adding field 'Book.book_series'
        db.add_column('book_book', 'book_series',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['book.Series'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Book.book_number'
        db.add_column('book_book', 'book_number',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=5, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Series'
        db.delete_table('book_series')

        # Deleting field 'Book.book_series'
        db.delete_column('book_book', 'book_series_id')

        # Deleting field 'Book.book_number'
        db.delete_column('book_book', 'book_number')


    models = {
        'book.author': {
            'Meta': {'object_name': 'Author'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'book.book': {
            'Meta': {'object_name': 'Book'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['book.Author']"}),
            'book_number': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'book_series': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['book.Series']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'format': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['book.Format']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isbn': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '15'}),
            'publication_year': ('django.db.models.fields.IntegerField', [], {}),
            'publisher': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['book.Publisher']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
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