from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Author(models.Model):
    name = models.CharField(max_length = 128)

    def __unicode__(self):
        return self.name

class Condition(models.Model):
    label = models.CharField(max_length = 16)

    def __unicode__(self):
        return self.label

class Format(models.Model):
    label = models.CharField(max_length = 32)

    def __unicode__(self):
        return self.label

class Publisher(models.Model):
    name = models.CharField(max_length = 64)

    def __unicode__(self):
        return self.name

class Series(models.Model):
    name = models.CharField(max_length = 64)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Series'
        verbose_name_plural = 'Series'

class Book(models.Model):
    title = models.CharField(max_length = 128)
    author = models.ForeignKey(Author)
    condition = models.ForeignKey(Condition, default = 7) # unknown
    format = models.ForeignKey(Format)
    location = models.CharField(max_length = 16, blank = True)
    publisher = models.ForeignKey(Publisher)
    series = models.ForeignKey(Series, null = True, blank = True)
    series_number = models.CharField(max_length = 5, blank = True)
    publication_year = models.IntegerField("Publication Year")
    isbn = models.CharField("ISBN", max_length = 15, default = '')
    description = models.TextField(default = '')
    updated_by = models.ForeignKey(User)
    updated_date = models.DateTimeField(default=datetime.now, blank=True)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.updated_date = datetime.now()

        super(Book, self).save(*args, **kwargs)

    class Meta:
        ordering = ['author__name', 'series__name', 'series_number', 'title']
