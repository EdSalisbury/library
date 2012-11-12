from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Developer(models.Model):
    name = models.CharField(max_length = 128)

    def __unicode__(self):
        return self.name

class Condition(models.Model):
    label = models.CharField(max_length = 16)

    def __unicode__(self):
        return self.label

class MediaType(models.Model):
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

class Platform(models.Model):
    name = models.CharField(max_length = 64)

    def __unicode__(self):
        return (self.name)

class VideoGame(models.Model):
    title = models.CharField(max_length = 128)
    developer = models.ForeignKey(Developer)
    condition = models.ForeignKey(Condition, default = 7) # unknown
    media_type = models.ForeignKey(MediaType)
    location = models.CharField(max_length = 16, blank = True)
    publisher = models.ForeignKey(Publisher)
    series = models.ForeignKey(Series, null = True, blank = True)
    series_number = models.CharField(max_length = 5, blank = True)
    publication_year = models.IntegerField("Publication Year")
    upc = models.CharField("UPC", max_length = 15, default = '')
    description = models.TextField(default = '')
    platform = models.ForeignKey(Platform)
    updated_by = models.ForeignKey(User)
    updated_date = models.DateTimeField(default=datetime.now, blank=True)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.updated_date = datetime.now()

        super(VideoGame, self).save(*args, **kwargs)

    class Meta:
        ordering = ['developer__name', 'publication_year', 'title']
        verbose_name = "Video Game"
