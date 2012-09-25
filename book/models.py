from django.db import models

class Author(models.Model):
    name = models.CharField(max_length = 128)

    def __unicode__(self):
        return self.name

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
    format = models.ForeignKey(Format)
    publisher = models.ForeignKey(Publisher)
    series = models.ForeignKey(Series, null = True, blank = True)
    series_number = models.CharField(max_length = 5, blank = True)
    publication_year = models.IntegerField("Publication Year")
    isbn = models.CharField("ISBN", max_length = 15, default = '')
    description = models.TextField(default = '')

    def __unicode__(self):
        return self.title

