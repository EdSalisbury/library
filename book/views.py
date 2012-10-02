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
import logging

logger = logging.getLogger(__name__)

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
    return render_to_response('book/view.html', {'book': book, 'img_url': img_url, 'tab': 'books', 'action': 'view'})

def get_author(name):
    name = unicode(name).encode('utf-8')
    try:
        author = Author.objects.get(name = name)
    except Author.DoesNotExist:
        author = Author.objects.create(name = name)
    return author

def get_publisher(name):
    name = unicode(name).encode('utf-8')
    try:
        publisher = Publisher.objects.get(name = name)
    except Publisher.DoesNotExist:
        publisher = Publisher.objects.create(name = name)
    return publisher

def get_series(name):
    if not name:
        return None
    name = unicode(name).encode('utf-8')
    try:
        series = Series.objects.get(name = name)
    except Series.DoesNotExist:
        series = Series.objects.create(name = name)
    return series

def get_binding_by_id(binding_id):
    binding = None
    try:
        binding = Format.objects.get(pk = binding_id)
    except Format.DoesNotExist:
        pass

    return binding

def get_binding_by_name(name):
    name = unicode(name).encode('utf-8')
    try:
        binding = Format.objects.get(label = name)
    except Format.DoesNotExist:
        binding = Format.objects.create(label = name)
    return binding

def get_condition_by_id(condition_id):
    condition = None
    try:
        condition = Condition.objects.get(pk = condition_id)
    except Condition.DoesNotExist:
        pass
    return condition

def get_condition_by_name(name):
    name = unicode(name).encode('utf-8')
    try:
        condition = Condition.objects.get(label = name)
    except Condition.DoesNotExist:
        condition = Condition.objects.create(label = name)
    return condition

def edit(request, book_id):
    c = {}
    c['tab'] = 'books'
    c['action'] = 'edit'
    c.update(csrf(request))

    if request.method == 'POST':
        post = request.POST
        logger.debug(post)
        title = unicode(post['title']).encode('utf-8')
        author = get_author(post['author'])
        series = get_series(post['series'])
        series_number = post['series_number']
        binding = get_binding_by_name(post['binding'])
        condition = get_condition_by_name(post['condition'])
        description = unicode(post['description']).encode('utf-8')
        publisher = get_publisher(post['publisher'])
        isbn = post['isbn']

        book = Book.objects.get(pk = book_id)
        book.title = title
        book.author = author
        book.series = series
        book.series_number = series_number
        book.format = binding
        book.condition = condition
        book.description = description
        book.publisher = publisher
        book.isbn = isbn

        book.save()
        c['updated'] = True

    c['book'] = get_object_or_404(Book, pk=book_id)
    c['bindings'] = Format.objects.all()
    c['conditions'] = Condition.objects.all()
    return render_to_response('book/edit.html', c)

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
