# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Condition'
        db.create_table('book_condition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=16)),
        ))
        db.send_create_signal('book', ['Condition'])

        # Adding field 'Book.condition'
        db.add_column('book_book', 'condition',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['book.Condition']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Condition'
        db.delete_table('book_condition')

        # Deleting field 'Book.condition'
        db.delete_column('book_book', 'condition_id')


    models = {
        'book.author': {
            'Meta': {'object_name': 'Author'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'book.book': {
            'Meta': {'object_name': 'Book'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['book.Author']"}),
            'condition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['book.Condition']"}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'format': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['book.Format']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isbn': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '15'}),
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