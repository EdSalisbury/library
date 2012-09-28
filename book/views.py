from django.core.context_processors import csrf
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpRequest
from django.conf import settings
from book.models import *
from vendor.controllers import AmazonController
import urllib
import HTMLParser
from types import *
import re

def list(request):
    book_list = Book.objects.all().order_by('title').order_by('publication_year').order_by('author__name')
    return render_to_response('book/list.html', {'book_list': book_list, 'tab': 'books'})

def catalog(request):
    book_list = Book.objects.all()
    return render_to_response('book/catalog.html', {'book_list': book_list, 'tab': 'books'})

def view(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    img_url = settings.MEDIA_URL + "book/" + str(book.id) + ".jpg"
    book.description = book.description.replace("\\'", "'")
    return render_to_response('book/view.html', {'book': book, 'img_url': img_url, 'tab': 'books'})

def add(request):
    return render_to_response('book/add.html', {'tab': 'books'})

def mass_add(request):
    c = {}
    c['tab'] = 'books'
    c.update(csrf(request))

    if request.method == 'POST':
        post = request.POST
        isbn = post['isbn']
        amazon = AmazonController()

        product = None

        if len(isbn) == 10:
            product = amazon.lookup(isbn)
        elif len(isbn) == 13:
            product = amazon.lookup(isbn, 'ISBN', 'Books')
#        elif len(isbn) == 12:
#            product = amazon.lookup(isbn, 'UPC', 'Books')

        if product:
            if type(product) is ListType:
                product = product[0]

            author_name = product.item.ItemAttributes.Author
            binding = product.item.ItemAttributes.Binding
            manufacturer = product.item.ItemAttributes.Manufacturer
            year = str(product.item.ItemAttributes.PublicationDate)[:4]

            try:
                publisher = Publisher.objects.get(name = manufacturer)
            except Publisher.DoesNotExist:
                publisher = Publisher.objects.create(
                    name = manufacturer
                )

            try:
                author = Author.objects.get(name = author_name)
            except Author.DoesNotExist:
                author = Author.objects.create(
                name = author_name
            )

            try:
                format = Format.objects.get(label = binding)
            except Format.DoesNotExist:
                format = Format.objects.create(
                    label = binding
                )

            desc = ""

            if len(product.item.EditorialReviews):
                desc = product.item.EditorialReviews[0].EditorialReview['Content']
                desc = unicode(desc).encode('utf-8')
                desc = re.sub('\'', '\\\'', desc)

            book = Book.objects.create(
                title = product.item.ItemAttributes.Title,
                author = author,
                format = format,
                publisher = publisher,
                publication_year = year,
                isbn = product.item.ItemAttributes.ISBN,
                description = desc,
                )

            image_url = str(product.item.LargeImage['URL'])
            urllib.urlretrieve(image_url, settings.MEDIA_ROOT + "/book/" + str(book.id) + ".jpg")

            c['status'] = product.item.ItemAttributes.Title + " has been added successfully."
        else:
            c['status'] = "Unable to find " + isbn + "."

    return render_to_response('book/mass_add.html', c)
