from django.contrib import admin
from book.models import *

class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'series', 'series_number', 'format', 'location', 'condition', 'publisher', 'publication_year')
    list_editable = ('title', 'format', 'location', 'condition', 'series', 'series_number')
    list_display_links = ('id',)

admin.site.register(Book, BookAdmin)
admin.site.register(Author)
admin.site.register(Format)
admin.site.register(Publisher)
admin.site.register(Series)
admin.site.register(Condition)
