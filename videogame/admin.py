from django.contrib import admin
from videogame.models import *

class VideoGameAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'platform', 'developer', 'series', 'series_number', 'media_type', 'location', 'condition', 'publisher', 'publication_year')
    list_editable = ('title', 'platform', 'media_type', 'location', 'condition', 'series', 'series_number')
    list_display_links = ('id',)

admin.site.register(VideoGame, VideoGameAdmin)
admin.site.register(Developer)
admin.site.register(MediaType)
admin.site.register(Publisher)
admin.site.register(Series)
admin.site.register(Condition)
admin.site.register(Platform)
