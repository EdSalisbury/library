# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Author'
        db.create_table('book_author', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('book', ['Author'])

        # Adding model 'Format'
        db.create_table('book_format', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('book', ['Format'])

        # Adding model 'Publisher'
        db.create_table('book_publisher', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('book', ['Publisher'])

        # Adding model 'Book'
        db.create_table('book_book', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['book.Author'])),
            ('format', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['book.Format'])),
            ('publisher', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['book.Publisher'])),
            ('publication_year', self.gf('django.db.models.fields.IntegerField')()),
            ('isbn', self.gf('django.db.models.fields.CharField')(default='', max_length=15)),
            ('description', self.gf('django.db.models.fields.TextField')(default='')),
        ))
        db.send_create_signal('book', ['Book'])


    def backwards(self, orm):
        # Deleting model 'Author'
        db.delete_table('book_author')

        # Deleting model 'Format'
        db.delete_table('book_format')

        # Deleting model 'Publisher'
        db.delete_table('book_publisher')

        # Deleting model 'Book'
        db.delete_table('book_book')


    models = {
        'book.author': {
            'Meta': {'object_name': 'Author'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'book.book': {
            'Meta': {'object_name': 'Book'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['book.Author']"}),
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
        }
    }

    complete_apps = ['book']