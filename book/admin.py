from django.contrib import admin
from book.models import *

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'format', 'condition', 'publisher', 'publication_year')

admin.site.register(Book, BookAdmin)
admin.site.register(Author)
admin.site.register(Format)
admin.site.register(Publisher)
admin.site.register(Series)
admin.site.register(Condition)
