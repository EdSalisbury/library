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
import inspect

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

def get_details(product):

    details = {}

    # Get publication year
    details['year'] = str(product.item.ItemAttributes.PublicationDate)[:4]

    # Get title
    title = product.item.ItemAttributes.Title
    title = unicode(title).encode('utf-8')
    details['title'] = re.sub('\'', '\\\'', title)

    # Get/create Publisher object
    manufacturer = product.item.ItemAttributes.Manufacturer
    try:
        details['publisher'] = Publisher.objects.get(name = manufacturer)
    except Publisher.DoesNotExist:
        details['publisher'] = Publisher.objects.create(
            name = manufacturer
        )

    # Get/create Author object
    author_name = product.item.ItemAttributes.Author
    author_name = unicode(author_name).encode('utf-8')
    author_name = re.sub('\'', '\\\'', author_name)
    try:
        details['author'] = Author.objects.get(name = author_name)
    except Author.DoesNotExist:
        details['author'] = Author.objects.create(
        name = author_name
    )

    # Get/create Format object
    binding = product.item.ItemAttributes.Binding
    try:
        details['format'] = Format.objects.get(label = binding)
    except Format.DoesNotExist:
        details['format'] = Format.objects.create(
            label = binding
        )

    # Get item description
    try:
        desc = product.item.EditorialReviews[0].EditorialReview['Content']
        desc = unicode(desc).encode('utf-8')
        details['desc'] = re.sub('\'', '\\\'', desc)
    except AttributeError:
        details['desc'] = ""

    return details

def mass_add(request):
    c = {}
    c['tab'] = 'books'
    c.update(csrf(request))

    if request.method == 'POST':
        post = request.POST
        isbn = post['isbn']
        amazon = AmazonController()

        product = None
        added = False

        if len(isbn) == 10:
            product = amazon.lookup(isbn)
        elif len(isbn) == 13:
            product = amazon.lookup(isbn, 'ISBN', 'Books')

        if product:
            if type(product) is ListType:
                product_list = product
            else:
                product_list = []
                product_list.append(product)

            for product in product_list:
                try:
                    product.item.LargeImage['URL']
                except AttributeError:
                    continue

                details = get_details(product)
                if not details['desc']:
                    continue

                book = Book.objects.create(
                    title = details['title'],
                    author = details['author'],
                    format = details['format'],
                    publisher = details['publisher'],
                    publication_year = details['year'],
                    isbn = isbn,
                    description = details['desc'],
                    )
                if book:
                    added = True

                # Get image
                try:
                    image_url = str(product.item.LargeImage['URL'])
                    urllib.urlretrieve(image_url, settings.MEDIA_ROOT + "/book/" + str(book.id) + ".jpg")
                except AttributeError:
                    pass

                c['book'] = book
                return render_to_response('book/mass_add.html', c)

        else:
            c['error'] = "Unable to find ISBN %s." % (isbn)

    return render_to_response('book/mass_add.html', c)
